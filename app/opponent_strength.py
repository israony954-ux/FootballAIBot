def calcular_forca_adversarios(jogos, team_id):
    """
    Calcula uma estimativa simples da força média dos adversários.

    Quanto maior a pontuação, maior a força média dos adversários
    enfrentados pelo time.
    """

    if not jogos:
        return {
            "jogos_avaliados": 0,
            "forca_media": 0
        }

    pontos = []

    for jogo in jogos:
        try:
            casa = jogo["teams"]["home"]
            fora = jogo["teams"]["away"]

            adversario = (
                fora
                if casa["id"] == team_id
                else casa
            )

            # O API-Football pode fornecer ranking/posição
            # em diferentes endpoints. Por enquanto usamos
            # somente dados disponíveis no próprio confronto.
            ranking = adversario.get("rank")

            if ranking is not None:
                ranking = float(ranking)

                # Converte posição em uma escala simples:
                # posição 1 = 100
                # posição 20 = 5
                forca = max(
                    5,
                    100 - ((ranking - 1) * 5)
                )

                pontos.append(forca)

        except (KeyError, TypeError, ValueError):
            continue

    if not pontos:
        return {
            "jogos_avaliados": 0,
            "forca_media": 0
        }

    return {
        "jogos_avaliados": len(pontos),
        "forca_media": round(
            sum(pontos) / len(pontos),
            1
        )
    }
