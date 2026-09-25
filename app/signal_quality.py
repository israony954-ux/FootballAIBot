def calcular_qualidade(amostra_casa, amostra_fora, amostra_h2h):
    pontos = 0

    if amostra_casa >= 10:
        pontos += 35
    elif amostra_casa >= 5:
        pontos += 25
    elif amostra_casa >= 3:
        pontos += 15

    if amostra_fora >= 10:
        pontos += 35
    elif amostra_fora >= 5:
        pontos += 25
    elif amostra_fora >= 3:
        pontos += 15

    if amostra_h2h >= 5:
        pontos += 30
    elif amostra_h2h >= 3:
        pontos += 20
    elif amostra_h2h >= 1:
        pontos += 10

    return min(pontos, 100)


if __name__ == "__main__":
    qualidade = calcular_qualidade(10, 10, 4)
    print("QUALIDADE DO SINAL:", qualidade)
