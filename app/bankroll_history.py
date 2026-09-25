import json
import os
from datetime import datetime


class BankrollHistory:
    def __init__(self, filepath="data/bankroll_history.json"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        directory = os.path.dirname(self.filepath)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=2)

    def load(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def record(self, bankroll, profit_loss, operation_type="resultado"):
        history = self.load()

        entry = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "tipo": operation_type,
            "banca": round(bankroll, 2),
            "resultado": round(profit_loss, 2),
        }

        history.append(entry)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=2)

        return entry

    def last(self):
        history = self.load()
        return history[-1] if history else None

    def total_operations(self):
        return len(self.load())
