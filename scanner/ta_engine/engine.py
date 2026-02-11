from typing import Dict
from scanner.ta_engine.context import TAContext
from scanner.ta_engine.rules import TARules


class TAEngine:
    """
    TA Engine skeleton.
    No alerting, no routing, no scoring.
    Only evaluate rule states.
    """

    def __init__(self):
        self.context = TAContext()
        self.rules = TARules()

    def process_candle(self, candle: Dict) -> Dict[str, bool]:
        """
        Add candle and evaluate rule states.
        """

        self.context.add_candle(candle)

        results = {
            "sma_cross": self.rules.rule_sma_cross(
                self.context, short_period=5, long_period=20
            ),
            "rsi_overbought": self.rules.rule_rsi_overbought(
                self.context, period=14, threshold=70
            ),
            "rsi_oversold": self.rules.rule_rsi_oversold(
                self.context, period=14, threshold=30
            ),
        }

        return results
