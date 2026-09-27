from app.bankroll_manager import BankrollConfig, BankrollManager
from app.football_api import FootballAPI
from app.complete_analysis import analisar_completo
from app.prediction_history import salvar_previsao
from app.report import gerar_relatorio
from app.global_radar import avaliar_jogo
from app.multiple_runner import executar_multipla
from datetime import datetime, timezone
banca = BankrollManager(BankrollConfig(50.0, 100.0, "gestao"))


def gerar_previsao(jogo):
    casa = jogo["teams"]["home"]
    fora = jogo["teams"]["away"]

    fixture_id = jogo["fixture"]["id"]

    resultado = analisar_completo(
        casa["id"],
        fora["id"]
    )

    analise = resultado["analise"]["analise"]

    mercado = analise["mercado_principal"]
    probabilidade = analise["probabilidade_principal"]

    competicao = (
        jogo.get("league", {}).get(
            "name",
            "Competicao desconhecida"
        )
    )

    radar = avaliar_jogo(
        competicao,
        resultado["qualidade_sinal"],
        probabilidade
    )
    stake = banca.calculate_stake(probabilidade)
    print(f"Stake sugerida: R$ {stake:.2f}")

    salvar_previsao(
        fixture_id,
        casa["name"],
        fora["name"],
        mercado,
        probabilidade,
        resultado["qualidade_sinal"]
    )

    gerar_relatorio(
        resultado,
        casa["name"],
        fora["name"],
        radar
    )

    return {
        "jogo": f'{casa["name"]} x {fora["name"]}',
        "mercados": analise["mercados"],
    }


def buscar_jogos_futuros():
    api = FootballAPI()

    hoje = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")

    jogos = api.buscar_jogos(hoje)

    agora = datetime.now(
        timezone.utc
    )

    futuros = []

    for jogo in jogos:
        try:
            data_jogo = datetime.fromisoformat(
                jogo["fixture"]["date"].replace(
                    "Z",
                    "+00:00"
                )
            )
        except (KeyError, ValueError):
            continue

        if data_jogo > agora:
            futuros.append(jogo)

    return futuros


def main():
    print("=" * 55)
    print("              FOOTBALL AI BOT")
    print("=" * 55)

    try:
        futuros = buscar_jogos_futuros()
    except Exception as erro:
        print()
        print("ERRO AO BUSCAR JOGOS:")
        print(erro)
        return

    print()
    print("JOGOS FUTUROS:", len(futuros))

    analises_multipla = []

    for jogo in futuros[:4]:
        try:
            analise_multipla = gerar_previsao(jogo)
            if analise_multipla:
                analises_multipla.append(analise_multipla)
        except Exception as erro:
            print()
            print("ERRO NO JOGO:", jogo.get("fixture", {}).get("id"))
            print("MOTIVO:", erro)
            if "API FOOTBALL LIMIT" in str(erro) or "limite de requisicoes atingido" in str(erro):
                print("API LIMITADA. Encerrando processamento.")
                break

    if analises_multipla:
        try:
            multipla = executar_multipla(analises_multipla)
            print()
            print("MULTIPLA GERADA:", multipla)
        except Exception as erro:
            print("ERRO AO GERAR MULTIPLA:", erro)

if __name__ == "__main__":
    main()
