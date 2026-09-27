from app.complete_analysis import analisar_completo
from app.multiple_runner import executar_multipla


def montar_multipla_jogos(jogos, minimo=0.70, limite=3):
    analises = []

    for jogo in jogos:
        casa = jogo["teams"]["home"]
        fora = jogo["teams"]["away"]

        resultado = analisar_completo(
            casa["id"],
            fora["id"]
        )

        analise = resultado["analise"]["analise"]

        analises.append({
            "jogo": f'{casa["name"]} x {fora["name"]}',
            "mercados": analise["mercados"]
        })

    return executar_multipla(
        analises,
        minimo=minimo,
        limite=limite
    )
