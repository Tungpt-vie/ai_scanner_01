from typing import Dict
from scanner.fa_gate.rules import FARules
from scanner.fa_gate.store import FAStatus


class FAEvaluator:
    """
    Apply FA rules and map to FAStatus.
    """

    def __init__(self, min_avg_value_traded: float):
        self.rules = FARules(min_avg_value_traded)

    def evaluate(self, symbol: str, data: Dict) -> FAStatus:
        """
        Return FAStatus for given symbol.
        """

        try:
            result = self.rules.evaluate(data)
        except Exception:
            print(f"[FA_GATE] FA_DATA_ERROR | symbol={symbol}")
            return FAStatus.FA_UNKNOWN

        if result == "PASS":
            print(f"[FA_GATE] FA_PASS | symbol={symbol}")
            return FAStatus.FA_PASS

        if result == "FAIL":
            print(f"[FA_GATE] FA_FAIL | symbol={symbol}")
            return FAStatus.FA_FAIL

        print(f"[FA_GATE] FA_UNKNOWN | symbol={symbol}")
        return FAStatus.FA_UNKNOWN
