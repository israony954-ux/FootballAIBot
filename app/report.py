def gerar_relatorio(
    resultado,
    nome_casa,
    nome_fora,
    radar=None,
    noticias=None
):
    analise = resultado["analise"]
    mercados = analise["analise"]["mercados"]

    print()
    print("=" * 55)
    print("              FOOTBALL AI BOT")
    print("=" * 55)
    print(f"JOGO: {nome_casa} x {nome_fora}")
    print("=" * 55)

    print()
    print("MERCADO PRINCIPAL")
    print("-" * 55)
    print(
        analise["analise"]["mercado_principal"],
        "-",
        round(
            analise["analise"]["probabilidade_principal"] * 100,
            1
        ),
        "%"
    )

    print()
    print("QUALIDADE DOS DADOS")
    print("-" * 55)
    print(
        resultado["qualidade_sinal"],
        "/100"
    )

    if radar:
        print()
        print("GLOBAL RADAR")
        print("-" * 55)
        print(
            "Competição:",
            radar.get("competicao", "N/A")
        )
        print(
            "Prioridade:",
            radar.get("prioridade", False)
        )
        print(
            "Força do sinal:",
            radar.get("forca_sinal", 0),
            "/100"
        )
        print(
            "Aprovado:",
            radar.get("aprovado", False)
        )

    if noticias:
        print()
        print("ESCALAÇÕES / DESFALQUES")
        print("-" * 55)

        casa = noticias.get("casa", {})
        fora = noticias.get("fora", {})

        print(
            nome_casa,
            "- ausências:",
            casa.get("total_ausencias", 0)
        )

        print(
            nome_fora,
            "- ausências:",
            fora.get("total_ausencias", 0)
        )

        print(
            "Qualidade da informação casa:",
            casa.get("qualidade_informacao", 0),
            "/100"
        )

        print(
            "Qualidade da informação fora:",
            fora.get("qualidade_informacao", 0),
            "/100"
        )

    print()
    print("AMOSTRAS")
    print("-" * 55)
    print(
        "Últimos jogos do mandante:",
        resultado["amostras"]["ultimos_casa"]
    )
    print(
        "Últimos jogos do visitante:",
        resultado["amostras"]["ultimos_fora"]
    )
    print(
        "H2H:",
        resultado["amostras"]["h2h"]
    )

    print()
    print("H2H COM RECÊNCIA")
    print("-" * 55)

    h2h_recencia = resultado["h2h"].get(
        "recencia",
        {}
    )

    print(
        "Jogos avaliados:",
        h2h_recencia.get(
            "jogos_avaliados",
            0
        )
    )

    print(
        "Média gols time 1:",
        h2h_recencia.get(
            "media_gols_time1",
            0
        )
    )

    print(
        "Média gols time 2:",
        h2h_recencia.get(
            "media_gols_time2",
            0
        )
    )

    print()
    print("MÉDIAS DE GOLS ESTIMADAS")
    print("-" * 55)
    print(
        "Mandante:",
        analise["medias_gols"]["casa"]
    )
    print(
        "Visitante:",
        analise["medias_gols"]["fora"]
    )

    print()
    print("FORÇA DOS ADVERSÁRIOS")
    print("-" * 55)

    for lado, dados in analise["forca_adversarios"].items():
        print(
            lado.upper() + ":",
            dados["forca_media"],
            "| jogos avaliados:",
            dados["jogos_avaliados"]
        )

    print()
    print("MERCADOS ANALISADOS")
    print("-" * 55)

    for mercado, probabilidade in mercados.items():
        print(
            f"{mercado}: {probabilidade * 100:.1f}%"
        )

    print()
    print("=" * 55)
    print("Probabilidades são estimativas estatísticas.")
    print("Não representam garantia de resultado.")
    print("=" * 55)
