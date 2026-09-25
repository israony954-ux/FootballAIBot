from math import exp, factorial


def poisson(k, media):
    if media <= 0:
        return 1.0 if k == 0 else 0.0

    return exp(-media) * (media ** k) / factorial(k)


def score_matrix(media_casa, media_fora, max_gols=8):
    matriz = {}

    for gols_casa in range(max_gols + 1):
        for gols_fora in range(max_gols + 1):
            prob_casa = poisson(gols_casa, media_casa)
            prob_fora = poisson(gols_fora, media_fora)

            matriz[(gols_casa, gols_fora)] = (
                prob_casa * prob_fora
            )

    return matriz


def analisar_jogo(media_casa, media_fora):
    matriz = score_matrix(
        media_casa,
        media_fora
    )

    casa = 0.0
    empate = 0.0
    fora = 0.0
    over_15 = 0.0
    over_25 = 0.0
    under_35 = 0.0
    ambas_marcam = 0.0

    for (gols_casa, gols_fora), probabilidade in matriz.items():

        if gols_casa > gols_fora:
            casa += probabilidade

        elif gols_casa == gols_fora:
            empate += probabilidade

        else:
            fora += probabilidade

        total_gols = gols_casa + gols_fora

        if total_gols >= 2:
            over_15 += probabilidade

        if total_gols >= 3:
            over_25 += probabilidade

        if total_gols <= 3:
            under_35 += probabilidade

        if gols_casa >= 1 and gols_fora >= 1:
            ambas_marcam += probabilidade

    mercados = {
        "Casa": casa,
        "Empate": empate,
        "Fora": fora,
        "Over 1.5 gols": over_15,
        "Over 2.5 gols": over_25,
        "Under 3.5 gols": under_35,
        "Ambas marcam": ambas_marcam
    }

    mercado_principal = max(
        mercados,
        key=mercados.get
    )

    return {
        "mercados": mercados,
        "mercado_principal": mercado_principal,
        "probabilidade_principal": mercados[
            mercado_principal
        ]
    }
