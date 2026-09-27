from app.multiple_builder import montar_multipla
from app.multiple_history import salvar_multipla


def executar_multipla(analises, minimo=0.70, limite=3):
    resultado = montar_multipla(
        analises,
        minimo=minimo,
        limite=limite,
    )

    if resultado["selecoes"]:
        salvar_multipla(
            resultado["selecoes"],
            resultado["probabilidade"],
        )

    return resultado


if __name__ == "__main__":
    print("MULTIPLE RUNNER OK")
