import os
import time
import json
import hashlib
import requests


class FootballAPI:
    BASE_URL = "https://v3.football.api-sports.io"
    CACHE_DIR = "data/api_cache"

    def __init__(self):
        self.api_key = os.getenv("API_FOOTBALL_KEY")

        if not self.api_key:
            raise RuntimeError("API_FOOTBALL_KEY nao encontrada.")

        self.headers = {
            "x-apisports-key": self.api_key
        }

        self.ultima_requisicao = 0
        self.intervalo_minimo = 3.0

        os.makedirs(self.CACHE_DIR, exist_ok=True)

    def _cache_path(self, endpoint, params):
        texto = endpoint + "|" + json.dumps(
            params or {},
            sort_keys=True
        )

        chave = hashlib.md5(
            texto.encode("utf-8")
        ).hexdigest()

        return os.path.join(
            self.CACHE_DIR,
            chave + ".json"
        )

    def _get(self, endpoint, params=None, cache_ttl=3600):
        caminho_cache = self._cache_path(
            endpoint,
            params
        )

        if os.path.exists(caminho_cache):
            idade = time.time() - os.path.getmtime(
                caminho_cache
            )

            if idade < cache_ttl:
                with open(
                    caminho_cache,
                    "r",
                    encoding="utf-8"
                ) as arquivo:
                    return json.load(arquivo)

        agora = time.time()

        espera = self.intervalo_minimo - (
            agora - self.ultima_requisicao
        )

        if espera > 0:
            time.sleep(espera)

        url = f"{self.BASE_URL}/{endpoint}"

        resposta = requests.get(
            url,
            headers=self.headers,
            params=params or {},
            timeout=30
        )

        self.ultima_requisicao = time.time()

        if resposta.status_code == 429:
            raise RuntimeError(
                "API_FOOTBALL_LIMIT: limite de requisicoes atingido."
            )

        resposta.raise_for_status()

        dados = resposta.json()

        erros = dados.get("errors")

        if erros:
            raise RuntimeError(
                f"Erro da API: {erros}"
            )

        resultado = dados.get("response", [])

        with open(
            caminho_cache,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                resultado,
                arquivo,
                ensure_ascii=False
            )

        return resultado

    def buscar_jogos(self, data):
        return self._get(
            "fixtures",
            {"date": data},
            cache_ttl=300
        )

    def buscar_jogo(self, fixture_id):
        jogos = self._get(
            "fixtures",
            {"id": fixture_id},
            cache_ttl=300
        )

        return jogos[0] if jogos else None

    def ultimos_jogos(
        self,
        team_id,
        limite=10,
        temporada=2024
    ):
        jogos = self._get(
            "fixtures",
            {
                "team": team_id,
                "season": temporada,
                "status": "FT"
            },
            cache_ttl=86400
        )

        jogos.sort(
            key=lambda jogo: jogo.get(
                "fixture",
                {}
            ).get(
                "date",
                ""
            ),
            reverse=True
        )

        return jogos[:limite]
