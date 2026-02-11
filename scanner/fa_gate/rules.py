from typing import Dict


class FARules:
    """
    Rule-based coarse FA filter.
    No scoring, no ranking.
    """

    def __init__(self, min_avg_value_traded: float):
        self.min_avg_value_traded = min_avg_value_traded

    def check_liquidity(self, data: Dict):
        value = data.get("avg_value_traded")

        if value is None:
            return None

        return value >= self.min_avg_value_traded

    def check_listing_status(self, data: Dict):
        suspended = data.get("is_suspended")
        delisting = data.get("is_delisting")

        if suspended is None or delisting is None:
            return None

        return not suspended and not delisting

    def check_profit_stability(self, data: Dict):
        profit_positive = data.get("profit_positive")

        if profit_positive is None:
            return None

        return profit_positive

    def evaluate(self, data: Dict) -> str:
        checks = [
            self.check_liquidity(data),
            self.check_listing_status(data),
            self.check_profit_stability(data),
        ]

        if any(result is False for result in checks):
            return "FAIL"

        if any(result is None for result in checks):
            return "UNKNOWN"

        return "PASS"
