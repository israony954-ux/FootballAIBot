from app.team_stats import calcular_estatisticas, separar_mando
from app.analyzer import analisar_jogo
from app.opponent_strength import calcular_forca_adversarios


def ajustar_por_forca(media, forca, ataque=True):
    """
    Ajusta levemente a média de gols conforme a força
    dos adversários.

    O ajuste é pequeno para evitar que uma amostra
    limitada domine o modelo.
    """

    if not forca or forca <= 0:
        return media

    referencia = 50
    diferenca = (forca - referencia) / 100

    if ataque:
        fator = 1 - (diferenca * 0.10)
    else:
        fator = 1 + (diferenca * 0.10)

    return max(0.15, media * fator)


def analisar_confronto(jogos_casa, jogos_fora, id_casa, id_fora, api=None):
    if api is None:
        from app.football_api import FootballAPI
        api = FootballAPI()
    stats_casa = calcular_estatisticas(
        jogos_casa,
        id_casa
    )

    stats_fora = calcular_estatisticas(
        jogos_fora,
        id_fora
    )

    mando_casa = separar_mando(
        jogos_casa,
        id_casa
    )

    mando_fora = separar_mando(
        jogos_fora,
        id_fora
    )

    stats_casa_mandante = calcular_estatisticas(
        mando_casa["casa"],
        id_casa
    )

    stats_fora_visitante = calcular_estatisticas(
        mando_fora["fora"],
        id_fora
    )

    forca_casa = calcular_forca_adversarios(
        jogos_casa,
        id_casa,
        api
    )

    forca_fora = calcular_forca_adversarios(
        jogos_fora,
        id_fora,
        api
    )

    ataque_casa = (
        stats_casa["media_gols_marcados"] * 0.40
        + stats_casa_mandante["media_gols_marcados"] * 0.60
    )

    defesa_casa = (
        stats_casa["media_gols_sofridos"] * 0.40
        + stats_casa_mandante["media_gols_sofridos"] * 0.60
    )

    ataque_fora = (
        stats_fora["media_gols_marcados"] * 0.40
        + stats_fora_visitante["media_gols_marcados"] * 0.60
    )

    defesa_fora = (
        stats_fora["media_gols_sofridos"] * 0.40
        + stats_fora_visitante["media_gols_sofridos"] * 0.60
    )

    ataque_casa = ajustar_por_forca(
        ataque_casa,
        forca_casa["forca_media"],
        ataque=True
    )

    ataque_fora = ajustar_por_forca(
        ataque_fora,
        forca_fora["forca_media"],
        ataque=True
    )

    media_casa = (
        ataque_casa * 0.60
        + defesa_fora * 0.40
    )

    media_fora = (
        ataque_fora * 0.60
        + defesa_casa * 0.40
    )

    resultado = analisar_jogo(
        media_casa,
        media_fora
    )

    return {
        "casa": stats_casa,
        "fora": stats_fora,
        "casa_mandante": stats_casa_mandante,
        "fora_visitante": stats_fora_visitante,
        "forca_adversarios": {
            "casa": forca_casa,
            "fora": forca_fora
        },
        "medias_gols": {
            "casa": round(media_casa, 2),
            "fora": round(media_fora, 2)
        },
        "analise": resultado
    }
