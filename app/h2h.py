from datetime import datetime, timezone
from math import exp

from app.football_api import FootballAPI


def calcular_peso_recencia(data_jogo, meia_vida_dias=365):
    """
    Quanto mais recente o confronto, maior o peso.
    A meia-vida padrão é de 365 dias.
    """

    if not data_jogo:
        return 0.0

    try:
        data = datetime.fromisoformat(
            data_jogo.replace("Z", "+00:00")
        )
    except ValueError:
        return 0.0

    agora = datetime.now(timezone.utc)

    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)

    dias = max(
        0,
        (agora - data).days
    )

    return exp(
        -dias / meia_vida_dias
    )


def buscar_h2h(id_time1, id_time2, limite=10):
    api = FootballAPI()

    jogos = api._get(
        "fixtures/headtohead",
        {
            "h2h": f"{id_time1}-{id_time2}"
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


def analisar_h2h(jogos, id_time1, id_time2):
    total = 0
    peso_total = 0.0

    vitorias = 0.0
    empates = 0.0
    derrotas = 0.0

    gols_time1 = 0.0
    gols_time2 = 0.0

    for jogo in jogos:
        try:
            data = jogo["fixture"]["date"]
            casa = jogo["teams"]["home"]["id"]
            fora = jogo["teams"]["away"]["id"]

            gols_casa = jogo["goals"]["home"]
            gols_fora = jogo["goals"]["away"]

            if gols_casa is None or gols_fora is None:
                continue

            peso = calcular_peso_recencia(data)

            if peso <= 0:
                continue

            if casa == id_time1:
                gols1 = gols_casa
                gols2 = gols_fora
            elif fora == id_time1:
                gols1 = gols_fora
                gols2 = gols_casa
            else:
                continue

            if gols1 > gols2:
                vitorias += peso
            elif gols1 == gols2:
                empates += peso
            else:
                derrotas += peso

            gols_time1 += gols1 * peso
            gols_time2 += gols2 * peso

            peso_total += peso
            total += 1

        except (KeyError, TypeError, ValueError):
            continue

    if peso_total == 0:
        return {
            "jogos_avaliados": 0,
            "peso_total": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "media_gols_time1": 0,
            "media_gols_time2": 0
        }

    return {
        "jogos_avaliados": total,
        "peso_total": round(peso_total, 3),
        "vitorias": round(
            vitorias / peso_total * 100,
            1
        ),
        "empates": round(
            empates / peso_total * 100,
            1
        ),
        "derrotas": round(
            derrotas / peso_total * 100,
            1
        ),
        "media_gols_time1": round(
            gols_time1 / peso_total,
            2
        ),
        "media_gols_time2": round(
            gols_time2 / peso_total,
            2
        )
    }


if __name__ == "__main__":
    jogos = buscar_h2h(127, 1153)

    resultado = analisar_h2h(
        jogos,
        127,
        1153
    )

    print("===================================")
    print("        H2H COM RECENCIA")
    print("===================================")
    print(
        "JOGOS AVALIADOS:",
        resultado["jogos_avaliados"]
    )
    print(
        "PESO TOTAL:",
        resultado["peso_total"]
    )
    print(
        "VITORIAS:",
        resultado["vitorias"],
        "%"
    )
    print(
        "EMPATES:",
        resultado["empates"],
        "%"
    )
    print(
        "DERROTAS:",
        resultado["derrotas"],
        "%"
    )
    print(
        "MEDIA GOLS TIME 1:",
        resultado["media_gols_time1"]
    )
    print(
        "MEDIA GOLS TIME 2:",
        resultado["media_gols_time2"]
    )
