import json
import os


CONFIG = "config/competitions.json"


def carregar_configuracao():
    if not os.path.exists(CONFIG):
        return {}

    with open(
        CONFIG,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)


def calcular_sinal(qualidade_dados, probabilidade):
    """
    Converte qualidade dos dados e probabilidade
    em uma força de sinal de 0 a 100.
    """

    qualidade = max(
        0,
        min(100, float(qualidade_dados))
    )

    probabilidade = max(
        0,
        min(1, float(probabilidade))
    )

    sinal = (
        qualidade * 0.45
        + (probabilidade * 100) * 0.55
    )

    return round(
        max(0, min(100, sinal)),
        1
    )


def avaliar_jogo(
    competicao,
    qualidade_dados,
    probabilidade
):
    config = carregar_configuracao()

    radar = config.get(
        "global_radar",
        {}
    )

    prioridade = competicao in config.get(
        "priority",
        []
    )

    sinal = calcular_sinal(
        qualidade_dados,
        probabilidade
    )

    qualidade_minima = radar.get(
        "minimum_data_quality",
        70
    )

    sinal_minimo = radar.get(
        "minimum_signal_strength",
        68
    )

    aprovado = (
        qualidade_dados >= qualidade_minima
        and sinal >= sinal_minimo
    )

    return {
        "competicao": competicao,
        "prioridade": prioridade,
        "qualidade_dados": qualidade_dados,
        "forca_sinal": sinal,
        "aprovado": aprovado
    }


if __name__ == "__main__":
    resultado = avaliar_jogo(
        "Exemplo League",
        80,
        0.75
    )

    print("===================================")
    print("         GLOBAL RADAR")
    print("===================================")
    print("COMPETICAO:", resultado["competicao"])
    print("PRIORIDADE:", resultado["prioridade"])
    print("QUALIDADE:", resultado["qualidade_dados"])
    print("FORCA DO SINAL:", resultado["forca_sinal"])
    print("APROVADO:", resultado["aprovado"])
