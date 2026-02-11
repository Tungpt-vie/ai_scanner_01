from scanner.ta_engine.indicators import Indicators
from scanner.ta_engine.context import TAContext


class TARules:
    """
    Deterministic TA rule set.
    No alert, no scoring, no optimization.
    """

    def __init__(self):
        pass

    def rule_sma_cross(self, context: TAContext, short_period: int, long_period: int) -> bool:
        """
        Short SMA crosses above Long SMA (simple check).
        """

        if context.size() < long_period:
            return False

        short_sma = Indicators.sma(context.closes, short_period)
        long_sma = Indicators.sma(context.closes, long_period)

        if short_sma is None or long_sma is None:
            return False

        return short_sma > long_sma

    def rule_rsi_overbought(self, context: TAContext, period: int, threshold: float) -> bool:
        """
        RSI above threshold.
        """

        rsi_value = Indicators.rsi(context.closes, period)

        if rsi_value is None:
            return False

        return rsi_value > threshold

    def rule_rsi_oversold(self, context: TAContext, period: int, threshold: float) -> bool:
        """
        RSI below threshold.
        """

        rsi_value = Indicators.rsi(context.closes, period)

        if rsi_value is None:
            return False

        return rsi_value < threshold

