import os

from app.bankroll_manager import BankrollConfig, BankrollManager


def main():
    print("===============================")
    print("        FOOTBALL AI BOT")
    print("===============================")
    print("Sistema pronto para receber dados de futebol.")

    chave = os.getenv("API_FOOTBALL_KEY")

    if chave:
        print("API_FOOTBALL_KEY: CHAVE ENCONTRADA")
    else:
        print("API_FOOTBALL_KEY: CHAVE NAO ENCONTRADA")

    config = BankrollConfig(
        initial_bankroll=50.0,
        target_bankroll=100.0,
        strategy="gestao",
    )

    banca = BankrollManager(config)

    print(f"Banca inicial: R$ {banca.bankroll:.2f}")
    print(f"Meta: R$ {config.target_bankroll:.2f}")
    print(f"Estrategia: {config.strategy}")
    print(f"Stake sugerida: R$ {banca.calculate_stake(0.8):.2f}")


if __name__ == "__main__":
    main()
