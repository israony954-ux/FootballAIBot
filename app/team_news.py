def analisar_desfalques(*args, **kwargs):
    return {
        "desfalques": [],
        "quantidade": 0,
        "impacto": 0.0,
    }


def comparar_elencos(noticias_casa=None, noticias_fora=None):
    return {
        "casa": noticias_casa or {},
        "fora": noticias_fora or {},
        "diferenca": 0.0,
    }
