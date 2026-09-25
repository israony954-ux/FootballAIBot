import json
import os


ARQUIVO = "data/prediction_history.jsonl"


def carregar_previsoes():
    if not os.path.exists(ARQUIVO):
        return []

    previsoes = []

    with open(
        ARQUIVO,
        "r",
        encoding="utf-8"
    ) as arquivo:

        for linha in arquivo:
            linha = linha.strip()

            if linha:
                previsoes.append(
                    json.loads(linha)
                )

    return previsoes


def avaliar():
    previsoes = carregar_previsoes()

    avaliadas = [
        p for p in previsoes
        if p.get("resultado_real") is not None
    ]

    if not avaliadas:
        print("NENHUMA PREVISAO AVALIADA.")
        return

    acertos = 0
    brier_total = 0.0

    for previsao in avaliadas:
        probabilidade = float(
            previsao["probabilidade"]
        )

        resultado = int(
            previsao["resultado_real"]
        )

        if resultado == 1:
            acertos += 1

        brier_total += (
            probabilidade - resultado
        ) ** 2

    total = len(avaliadas)

    taxa_acerto = (
        acertos / total * 100
    )

    brier_score = (
        brier_total / total
    )

    print("===================================")
    print("       AVALIACAO DO MODELO")
    print("===================================")
    print("PREVISOES AVALIADAS:", total)
    print("ACERTOS:", acertos)
    print(
        "TAXA DE ACERTO:",
        round(taxa_acerto, 2),
        "%"
    )
    print(
        "BRIER SCORE:",
        round(brier_score, 4)
    )


if __name__ == "__main__":
    avaliar()
