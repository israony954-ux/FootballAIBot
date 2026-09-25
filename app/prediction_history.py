import json
import os
from datetime import datetime, timezone

ARQUIVO = "data/prediction_history.jsonl"


def carregar_previsoes():
    if not os.path.exists(ARQUIVO):
        return []

    previsoes = []

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if linha:
                previsoes.append(json.loads(linha))

    return previsoes


def salvar_previsao(
    fixture_id,
    time_casa,
    time_fora,
    mercado,
    probabilidade,
    qualidade_dados
):
    os.makedirs("data", exist_ok=True)

    previsoes = carregar_previsoes()

    for previsao in previsoes:
        mesmo_jogo = previsao.get("fixture_id") == fixture_id
        mesmo_mercado = previsao.get("mercado") == mercado

        if mesmo_jogo and mesmo_mercado:
            return previsao

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fixture_id": fixture_id,
        "time_casa": time_casa,
        "time_fora": time_fora,
        "mercado": mercado,
        "probabilidade": probabilidade,
        "qualidade_dados": qualidade_dados,
        "resultado_real": None
    }

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

    return registro


def registrar_resultado(indice, resultado):
    previsoes = carregar_previsoes()

    if indice < 0 or indice >= len(previsoes):
        return False

    previsoes[indice]["resultado_real"] = resultado

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        for previsao in previsoes:
            arquivo.write(
                json.dumps(previsao, ensure_ascii=False) + "\n"
            )

    return True


if __name__ == "__main__":
    print("PREVISOES:", len(carregar_previsoes()))
