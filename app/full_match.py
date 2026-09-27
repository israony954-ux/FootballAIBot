from app.football_api import FootballAPI
from app.match_analysis import analisar_confronto
from app.history import ultimos_jogos_do_time


def analisar_por_ids(
    id_casa,
    id_fora,
    temporada=None
):
    api = FootballAPI()

    try:
        jogos_casa = api.ultimos_jogos(
            id_casa,
            10,
            temporada
        )
    except RuntimeError:
        jogos_casa = ultimos_jogos_do_time(
            id_casa,
            10,
            temporada
        )

    try:
        jogos_fora = api.ultimos_jogos(
            id_fora,
            10,
            temporada
        )
    except RuntimeError:
        jogos_fora = ultimos_jogos_do_time(
            id_fora,
            10,
            temporada
        )

    resultado = analisar_confronto(
        jogos_casa,
        jogos_fora,
        id_casa,
        id_fora
    )

    return resultado


if __name__ == "__main__":
    resultado = analisar_por_ids(
        127,
        1153
    )

    print("===================================")
    print("       ANALISE DO CONFRONTO")
    print("===================================")

    print(
        "MEDIA DE GOLS CASA:",
        resultado["medias_gols"]["casa"]
    )

    print(
        "MEDIA DE GOLS FORA:",
        resultado["medias_gols"]["fora"]
    )

    print(
        "MERCADO PRINCIPAL:",
        resultado["analise"]["mercado_principal"]
    )

    print(
        "PROBABILIDADE:",
        round(
            resultado["analise"][
                "probabilidade_principal"
            ] * 100,
            1
        ),
        "%"
    )

    print("===================================")
    print("MERCADOS")

    for mercado, probabilidade in resultado[
        "analise"
    ]["mercados"].items():

        print(
            mercado,
            ":",
            round(
                probabilidade * 100,
                1
            ),
            "%"
        )
