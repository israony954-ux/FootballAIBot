import json
import os
from datetime import datetime, timezone

ARQUIVO = "data/multiple_history.jsonl"


def salvar_multipla(selecoes, probabilidade):
    os.makedirs("data", exist_ok=True)

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "selecoes": selecoes,
        "probabilidade_aproximada": probabilidade,
        "resultado_real": None
    }

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            json.dumps(
                registro,
                ensure_ascii=False
            ) + "\n"
        )

    return registro


def carregar_multiplas():
    if not os.path.exists(ARQUIVO):
        return []

    registros = []

    with open(
        ARQUIVO,
        "r",
        encoding="utf-8"
    ) as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if linha:
                registros.append(
                    json.loads(linha)
                )

    return registros


def registrar_resultado(indice, resultado):
    registros = carregar_multiplas()

    if indice < 0 or indice >= len(registros):
        return False

    registros[indice]["resultado_real"] = resultado

    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as arquivo:
        for registro in registros:
            arquivo.write(
                json.dumps(
                    registro,
                    ensure_ascii=False
                ) + "\n"
            )

    return True


if __name__ == "__main__":
    teste = salvar_multipla(
        [
            {
                "jogo": "Teste A x Teste B",
                "mercado": "Over 1.5 gols",
                "probabilidade": 0.80
            }
        ],
        0.80
    )

    print("===================================")
    print("       MULTIPLE HISTORY")
    print("===================================")
    print("REGISTRO CRIADO: OK")
    print("SELECOES:", len(teste["selecoes"]))

    # Remove o registro de teste para não contaminar
    # o histórico real do modelo.
    registros = carregar_multiplas()

    if registros:
        registros = registros[:-1]

        with open(
            ARQUIVO,
            "w",
            encoding="utf-8"
        ) as arquivo:
            for registro in registros:
                arquivo.write(
                    json.dumps(
                        registro,
                        ensure_ascii=False
                    ) + "\n"
                )
