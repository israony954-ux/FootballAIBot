from dataclasses import dataclass, asdict
from typing import Dict

from app.bankroll_history import BankrollHistory


@dataclass
class BankrollConfig:
    initial_bankroll: float
    target_bankroll: float
    strategy: str = "gestao"

    def validate(self):
        if self.initial_bankroll < 50:
            raise ValueError("A banca inicial mínima é R$50.")

        if self.initial_bankroll > 100:
            raise ValueError("A banca inicial máxima é R$100.")

        if self.target_bankroll <= self.initial_bankroll:
            raise ValueError("A meta precisa ser maior que a banca inicial.")

        if self.strategy not in {"gestao", "controlada", "agressiva"}:
            raise ValueError("Estratégia inválida.")


class BankrollManager:
    MAX_RISK = {
        "gestao": 0.02,
        "controlada": 0.04,
        "agressiva": 0.08,
    }

    def __init__(self, config: BankrollConfig):
        config.validate()

        self.config = config
        self.history = BankrollHistory()

        last = self.history.last()

        if last:
            self.bankroll = float(last["banca"])
            self.operations = self.history.total_operations()
        else:
            self.bankroll = float(config.initial_bankroll)
            self.operations = 0

        self.peak_bankroll = self.bankroll
        self.total_profit = round(
            self.bankroll - config.initial_bankroll,
            2,
        )

    def calculate_stake(self, confidence: float = 0.0) -> float:
        confidence = max(0.0, min(1.0, confidence))

        max_risk = self.MAX_RISK[self.config.strategy]
        risk_factor = 0.50 + (confidence * 0.50)

        stake = self.bankroll * max_risk * risk_factor

        return round(
            max(0.01, min(stake, self.bankroll)),
            2,
        )

    def register_result(
        self,
        profit_loss: float,
        operation_type: str = "resultado",
    ) -> Dict:

        self.bankroll = round(
            self.bankroll + profit_loss,
            2,
        )

        self.total_profit = round(
            self.bankroll - self.config.initial_bankroll,
            2,
        )

        self.operations += 1

        if self.bankroll > self.peak_bankroll:
            self.peak_bankroll = self.bankroll

        self.history.record(
            bankroll=self.bankroll,
            profit_loss=profit_loss,
            operation_type=operation_type,
        )

        return self.status()

    def progress(self) -> float:
        target_gain = (
            self.config.target_bankroll
            - self.config.initial_bankroll
        )

        if target_gain <= 0:
            return 100.0

        current_gain = (
            self.bankroll
            - self.config.initial_bankroll
        )

        return round(
            max(
                0.0,
                min(
                    100.0,
                    (current_gain / target_gain) * 100,
                ),
            ),
            2,
        )

    def remaining_to_target(self) -> float:
        return round(
            max(
                0.0,
                self.config.target_bankroll
                - self.bankroll,
            ),
            2,
        )

    def drawdown(self) -> float:
        if self.peak_bankroll <= 0:
            return 0.0

        return round(
            max(
                0.0,
                (
                    (self.peak_bankroll - self.bankroll)
                    / self.peak_bankroll
                ) * 100,
            ),
            2,
        )

    def target_reached(self) -> bool:
        return self.bankroll >= self.config.target_bankroll

    def status(self) -> Dict:
        return {
            "banca_inicial": self.config.initial_bankroll,
            "banca_atual": self.bankroll,
            "meta": self.config.target_bankroll,
            "estrategia": self.config.strategy,
            "progresso_percentual": self.progress(),
            "faltante_para_meta": self.remaining_to_target(),
            "lucro_prejuizo": self.total_profit,
            "operacoes": self.operations,
            "pico_da_banca": self.peak_bankroll,
            "drawdown_percentual": self.drawdown(),
            "meta_atingida": self.target_reached(),
        }

    def export(self) -> Dict:
        return {
            "config": asdict(self.config),
            "status": self.status(),
        }
