def calcular_multipla(selecoes):
    """
    Calcula uma probabilidade aproximada para uma múltipla.

    Cada seleção deve ter:
    {
        "jogo": "...",
        "mercado": "...",
        "probabilidade": 0.80
    }

    IMPORTANTE:
    A multiplicação assume independência entre os eventos.
    Isso é apenas uma aproximação inicial.
    """

    if not selecoes:
        return {
            "selecoes": [],
            "probabilidade": 0.0
        }

    probabilidade = 1.0

    for selecao in selecoes:
        p = float(
            selecao.get(
                "probabilidade",
                0
            )
        )

        p = max(
            0.0,
            min(1.0, p)
        )

        probabilidade *= p

    return {
        "selecoes": selecoes,
        "probabilidade": round(
            probabilidade,
            6
        )
    }


def selecionar_melhores(
    mercados,
    minimo_probabilidade=0.70,
    limite=3
):
    """
    Seleciona até 'limite' mercados acima
    da probabilidade mínima.

    Não representa recomendação de aposta.
    É apenas uma seleção estatística para
    o motor de múltiplas.
    """

    candidatos = []

    for mercado in mercados:
        try:
            probabilidade = float(
                mercado["probabilidade"]
            )
        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

        if probabilidade >= minimo_probabilidade:
            candidatos.append(
                mercado
            )

    candidatos.sort(
        key=lambda item: item["probabilidade"],
        reverse=True
    )

    return candidatos[:limite]


if __name__ == "__main__":
    selecoes = [
        {
            "jogo": "Jogo A",
            "mercado": "Over 1.5 gols",
            "probabilidade": 0.82
        },
        {
            "jogo": "Jogo B",
            "mercado": "Over 1.5 gols",
            "probabilidade": 0.79
        },
        {
            "jogo": "Jogo C",
            "mercado": "Under 3.5 gols",
            "probabilidade": 0.76
        }
    ]

    resultado = calcular_multipla(
        selecoes
    )

    print("===================================")
    print("          MULTIPLAS")
    print("===================================")

    print(
        "SELECOES:",
        len(resultado["selecoes"])
    )

    print(
        "PROBABILIDADE APROXIMADA:",
        resultado["probabilidade"] * 100,
        "%"
    )

    print()
    print(
        "OBS: cálculo inicial por independência."
    )
