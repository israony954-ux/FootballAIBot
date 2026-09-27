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
            if os.path.exists(caminho_cache):
                try:
                    with open(
                        caminho_cache,
                        "r",
                        encoding="utf-8"
                    ) as arquivo:
                        print(
                            "API LIMITADA - usando cache:",
                            caminho_cache
                        )
                        return json.load(arquivo)
                except (json.JSONDecodeError, OSError):
                    pass

            raise RuntimeError(
                "API_FOOTBALL_LIMIT: limite de requisicoes atingido."
            )

        resposta.raise_for_status()

        dados = resposta.json()

        erros = dados.get("errors")

        if erros:
            erro_texto = str(erros).lower()

            if (
                "request limit" in erro_texto
                or "limit for the day" in erro_texto
                or "rate limit" in erro_texto
            ):
                if os.path.exists(caminho_cache):
                    try:
                        with open(
                            caminho_cache,
                            "r",
                            encoding="utf-8"
                        ) as arquivo:
                            print(
                                "API LIMITADA - usando cache antigo:",
                                caminho_cache
                            )
                            return json.load(arquivo)
                    except (json.JSONDecodeError, OSError):
                        pass

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
            cache_ttl=3600
        )

    def buscar_jogo(self, fixture_id):
        # Procura primeiro em todos os caches locais.
        fixture_id = str(fixture_id)

        try:
            for nome in os.listdir(self.CACHE_DIR):
                if not nome.endswith(".json"):
                    continue

                caminho = os.path.join(self.CACHE_DIR, nome)

                try:
                    with open(caminho, "r", encoding="utf-8") as arquivo_cache:
                        dados = json.load(arquivo_cache)
                except (json.JSONDecodeError, OSError):
                    continue

                if isinstance(dados, list):
                    jogos_cache = dados
                elif isinstance(dados, dict):
                    jogos_cache = dados.get("response", [])
                    if not isinstance(jogos_cache, list):
                        jogos_cache = [dados]
                else:
                    continue

                for jogo in jogos_cache:
                    if not isinstance(jogo, dict):
                        continue

                    fid = jogo.get("fixture", {}).get("id")

                    if str(fid) == fixture_id:
                        print("CACHE LOCAL - jogo encontrado:", fixture_id)
                        return jogo

        except OSError:
            pass

        # Se não encontrou no cache, consulta a API.
        jogos = self._get(
            "fixtures",
            {"id": fixture_id},
            cache_ttl=300
        )

        return jogos[0] if jogos else None

    def buscar_classificacao(self, league_id, temporada=None):
        return self._get(
            "standings",
            {"league": league_id, "season": temporada},
            cache_ttl=86400
        )

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
