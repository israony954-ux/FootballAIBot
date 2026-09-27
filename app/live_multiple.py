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

if __name__ == "__main__":
    from datetime import datetime
    from app.football_api import FootballAPI

    print("=== LIVE MULTIPLE ===")

    api = FootballAPI()
    data = datetime.now().strftime("%Y-%m-%d")

    jogos = api.buscar_jogos(data) or []

    status_live = {
        "1H", "2H", "HT", "ET", "BT", "P", "LIVE"
    }

    jogos_live = [
        jogo for jogo in jogos
        if jogo.get("fixture", {}).get("status", {}).get("short") in status_live
    ]

    print("Jogos encontrados:", len(jogos))
    print("Jogos ao vivo:", len(jogos_live))

    if not jogos_live:
        print("Nenhum jogo ao vivo encontrado no momento.")
    else:
        resultado = montar_multipla_jogos(
            jogos_live[:10],
            minimo=0.70,
            limite=3
        )

        print("MULTIPLA AO VIVO:")
        print(resultado)
