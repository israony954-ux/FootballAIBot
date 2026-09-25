def calcular_estatisticas(jogos, team_id):
    validos = []

    for jogo in jogos:
        try:
            gols_casa = jogo["goals"]["home"]
            gols_fora = jogo["goals"]["away"]

            if gols_casa is None or gols_fora is None:
                continue

            validos.append(jogo)

        except (KeyError, TypeError):
            continue

    total = len(validos)

    if total == 0:
        return {
            "jogos": 0,
            "gols_marcados": 0,
            "gols_sofridos": 0,
            "media_gols_marcados": 0,
            "media_gols_sofridos": 0,
            "over_05": 0,
            "over_15": 0,
            "over_25": 0,
            "over_35": 0,
            "under_15": 0,
            "under_25": 0,
            "under_35": 0,
            "ambas_marcam": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0
        }

    gols_marcados = 0
    gols_sofridos = 0
    over_05 = 0
    over_15 = 0
    over_25 = 0
    over_35 = 0
    under_15 = 0
    under_25 = 0
    under_35 = 0
    ambas_marcam = 0
    vitorias = 0
    empates = 0
    derrotas = 0

    for jogo in validos:
        casa = jogo["teams"]["home"]
        fora = jogo["teams"]["away"]

        gols_casa = jogo["goals"]["home"]
        gols_fora = jogo["goals"]["away"]

        if casa["id"] == team_id:
            marcados = gols_casa
            sofridos = gols_fora

            if gols_casa > gols_fora:
                vitorias += 1
            elif gols_casa == gols_fora:
                empates += 1
            else:
                derrotas += 1
        else:
            marcados = gols_fora
            sofridos = gols_casa

            if gols_fora > gols_casa:
                vitorias += 1
            elif gols_fora == gols_casa:
                empates += 1
            else:
                derrotas += 1

        gols_marcados += marcados
        gols_sofridos += sofridos

        total_gols = gols_casa + gols_fora

        if total_gols >= 1:
            over_05 += 1

        if total_gols >= 2:
            over_15 += 1

        if total_gols >= 3:
            over_25 += 1

        if total_gols >= 4:
            over_35 += 1

        if total_gols <= 1:
            under_15 += 1

        if total_gols <= 2:
            under_25 += 1

        if total_gols <= 3:
            under_35 += 1

        if gols_casa >= 1 and gols_fora >= 1:
            ambas_marcam += 1

    return {
        "jogos": total,
        "gols_marcados": gols_marcados,
        "gols_sofridos": gols_sofridos,
        "media_gols_marcados": round(gols_marcados / total, 2),
        "media_gols_sofridos": round(gols_sofridos / total, 2),
        "over_05": round(over_05 / total * 100, 1),
        "over_15": round(over_15 / total * 100, 1),
        "over_25": round(over_25 / total * 100, 1),
        "over_35": round(over_35 / total * 100, 1),
        "under_15": round(under_15 / total * 100, 1),
        "under_25": round(under_25 / total * 100, 1),
        "under_35": round(under_35 / total * 100, 1),
        "ambas_marcam": round(ambas_marcam / total * 100, 1),
        "vitorias": round(vitorias / total * 100, 1),
        "empates": round(empates / total * 100, 1),
        "derrotas": round(derrotas / total * 100, 1)
    }


def separar_mando(jogos, team_id):
    """
    Separa os jogos do time em:
    - casa
    - fora
    """

    casa = []
    fora = []

    for jogo in jogos:
        try:
            if jogo["teams"]["home"]["id"] == team_id:
                casa.append(jogo)
            elif jogo["teams"]["away"]["id"] == team_id:
                fora.append(jogo)
        except (KeyError, TypeError):
            continue

    return {
        "casa": casa,
        "fora": fora
    }
