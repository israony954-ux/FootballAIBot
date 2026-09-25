import json
import os


ARQUIVO = "data/historico_jogos.json"


def carregar_historico():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_jogo(jogo):
    historico = carregar_historico()

    fixture_id = jogo.get("fixture", {}).get("id")

    if fixture_id is None:
        return False

    if any(item.get("fixture", {}).get("id") == fixture_id for item in historico):
        return False

    historico.append(jogo)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=2)

    return True


def ultimos_jogos_do_time(team_id, limite=10):
    historico = carregar_historico()

    jogos = []

    for jogo in historico:
        times = jogo.get("teams", {})

        casa = times.get("home", {}).get("id")
        fora = times.get("away", {}).get("id")

        if team_id == casa or team_id == fora:
            jogos.append(jogo)

    jogos.sort(
        key=lambda jogo: jogo.get("fixture", {}).get("date", ""),
        reverse=True
    )

    return jogos[:limite]
