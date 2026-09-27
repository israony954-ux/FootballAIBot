def calcular_forca_adversarios(jogos, team_id, api=None):
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
    classificacoes = {}

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

            if ranking is None and api is not None:
                liga = jogo.get("league", {})
                league_id = liga.get("id")
                temporada = liga.get("season", 2024)
                chave = (league_id, temporada)

                if league_id is not None:
                    if chave not in classificacoes:
                        try:
                            classificacoes[chave] = api.buscar_classificacao(league_id, temporada)
                        except Exception:
                            classificacoes[chave] = []

                    for resposta in classificacoes[chave]:
                        tabela = resposta.get("league", {}).get("standings", [])
                        if tabela and isinstance(tabela[0], list):
                            tabela = tabela[0]
                        for item in tabela:
                            if item.get("team", {}).get("id") == adversario.get("id"):
                                ranking = item.get("rank")
                                break
                        if ranking is not None:
                            break

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
