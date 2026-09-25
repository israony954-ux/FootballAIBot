from app.football_api import FootballAPI


def buscar_time_por_nome(nome):
    api = FootballAPI()

    resultados = api._get(
        "teams",
        {"search": nome}
    )

    if not resultados:
        return None

    return resultados[0]


if __name__ == "__main__":
    time = buscar_time_por_nome("Flamengo")

    if time:
        print("TIME:", time["team"]["name"])
        print("ID:", time["team"]["id"])
    else:
        print("TIME NAO ENCONTRADO")
