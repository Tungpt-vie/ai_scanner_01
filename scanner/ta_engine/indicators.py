from typing import List


class Indicators:
    """
    Basic deterministic TA indicators.
    """

    @staticmethod
    def sma(values: List[float], period: int):
        if len(values) < period or period <= 0:
            return None

        window = values[-period:]
        return sum(window) / period

    @staticmethod
    def ema(values: List[float], period: int):
        if len(values) < period or period <= 0:
            return None

        multiplier = 2 / (period + 1)
        ema_value = values[0]

        for price in values[1:]:
            ema_value = (price - ema_value) * multiplier + ema_value

        return ema_value

    @staticmethod
    def rsi(values: List[float], period: int):
        if len(values) <= period or period <= 0:
            return None

        gains = []
        losses = []

        for i in range(-period, 0):
            delta = values[i] - values[i - 1]

            if delta > 0:
                gains.append(delta)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(delta))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi
