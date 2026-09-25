from app.multiples import calcular_multipla


def montar_multipla(analises, minimo=0.70, limite=3):
    candidatos = []

    for analise in analises:
        jogo = analise.get("jogo", "Jogo desconhecido")
        mercados = analise.get("mercados", {})

        for mercado, probabilidade in mercados.items():
            try:
                probabilidade = float(probabilidade)
            except (TypeError, ValueError):
                continue

            if probabilidade >= minimo:
                candidatos.append({
                    "jogo": jogo,
                    "mercado": mercado,
                    "probabilidade": probabilidade
                })

    candidatos.sort(
        key=lambda item: item["probabilidade"],
        reverse=True
    )

    selecionados = []
    jogos_usados = set()

    for candidato in candidatos:
        jogo = candidato["jogo"]

        if jogo in jogos_usados:
            continue

        selecionados.append({
            **candidato,
            "probabilidade": candidato["probabilidade"]
        })

        jogos_usados.add(jogo)

        if len(selecionados) >= limite:
            break

    return calcular_multipla(selecionados)


if __name__ == "__main__":
    analises = [
        {
            "jogo": "Time A x Time B",
            "mercados": {
                "Over 1.5 gols": 0.82,
                "Ambas marcam": 0.61
            }
        },
        {
            "jogo": "Time C x Time D",
            "mercados": {
                "Over 1.5 gols": 0.79,
                "Under 3.5 gols": 0.76
            }
        },
        {
            "jogo": "Time E x Time F",
            "mercados": {
                "Casa": 0.74,
                "Over 2.5 gols": 0.55
            }
        }
    ]

    resultado = montar_multipla(analises)

    print("===================================")
    print("       MULTIPLE BUILDER")
    print("===================================")

    for selecao in resultado["selecoes"]:
        print(
            f'{selecao["jogo"]} | '
            f'{selecao["mercado"]} | '
            f'{selecao["probabilidade"] * 100:.1f}%'
        )

    print()
    print(
        "PROBABILIDADE APROXIMADA DA MULTIPLA:",
        f'{resultado["probabilidade"] * 100:.2f}%'
    )
    print()
    print(
        "OBS: ainda não considera correlação entre mercados."
    )
