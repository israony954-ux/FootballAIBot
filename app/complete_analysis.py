from datetime import datetime

from app.football_api import FootballAPI
from app.history import ultimos_jogos_do_time, salvar_jogo
from app.match_analysis import analisar_confronto
from app.h2h import buscar_h2h, analisar_h2h
from app.team_stats import calcular_estatisticas
from app.signal_quality import calcular_qualidade
from app.team_news import analisar_desfalques, comparar_elencos


def temporada_atual():
    """
    Retorna o ano atual.
    Para competições cujo calendário atravessa
    dois anos, o ajuste específico poderá ser
    feito posteriormente por competição.
    """
    return 2024


def analisar_completo(
    id_casa,
    id_fora,
    temporada=None,
    noticias_casa=None,
    noticias_fora=None
):
    if temporada is None:
        temporada = temporada_atual()

    api = FootballAPI()

    jogos_casa = ultimos_jogos_do_time(id_casa, 10)
    jogos_fora = ultimos_jogos_do_time(id_fora, 10)

    if not jogos_casa:
        jogos_casa = api.ultimos_jogos(id_casa, 10, temporada)
        for jogo in jogos_casa: salvar_jogo(jogo)

    if not jogos_fora:
        jogos_fora = api.ultimos_jogos(id_fora, 10, temporada)
        for jogo in jogos_fora: salvar_jogo(jogo)

    analise = analisar_confronto(
        jogos_casa,
        jogos_fora,
        id_casa,
        id_fora
    )

    h2h = buscar_h2h(
        id_casa,
        id_fora,
        10
    )

    estatisticas_h2h = calcular_estatisticas(
        h2h,
        id_casa
    )

    h2h_recencia = analisar_h2h(
        h2h,
        id_casa,
        id_fora
    )

    noticias_casa = analisar_desfalques(
        **(noticias_casa or {})
    )

    noticias_fora = analisar_desfalques(
        **(noticias_fora or {})
    )

    comparacao_elencos = comparar_elencos(
        noticias_casa,
        noticias_fora
    )

    qualidade = calcular_qualidade(
        len(jogos_casa),
        len(jogos_fora),
        len(h2h)
    )

    return {
        "temporada": temporada,
        "analise": analise,
        "amostras": {
            "ultimos_casa": len(jogos_casa),
            "ultimos_fora": len(jogos_fora),
            "h2h": len(h2h)
        },
        "h2h": {
            "jogos": len(h2h),
            "estatisticas": estatisticas_h2h,
            "recencia": h2h_recencia
        },
        "team_news": {
            "casa": noticias_casa,
            "fora": noticias_fora,
            "comparacao": comparacao_elencos
        },
        "qualidade_sinal": qualidade
    }
