from app.bankroll_manager import BankrollConfig, BankrollManager
from app.football_api import FootballAPI
from app.complete_analysis import analisar_completo
from app.prediction_history import salvar_previsao
from app.report import gerar_relatorio
from app.global_radar import avaliar_jogo
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

    for jogo in futuros[:4]:
        try:
            gerar_previsao(jogo)
        except Exception as erro:
            print()
            print("ERRO NO JOGO:", jogo.get("fixture", {}).get("id"))
            print("MOTIVO:", erro)
            if "API FOOTBALL LIMIT" in str(erro) or "limite de requisicoes atingido" in str(erro):
                print("API LIMITADA. Encerrando processamento.")
                break

if __name__ == "__main__":
    main()
