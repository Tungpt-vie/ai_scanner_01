from typing import List, Dict


class MeasurementExtractor:
    """
    Extract numeric measurements only.
    No narrative, no inference.
    """

    def __init__(self):
        pass

    def rsi_value(self, closes: List[float], period: int = 14):
        if len(closes) <= period:
            return None

        gains = []
        losses = []

        for i in range(-period, 0):
            delta = closes[i] - closes[i - 1]

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
        return 100 - (100 / (1 + rs))

    def volume_ratio(self, volumes: List[float], lookback: int = 20):
        if len(volumes) < lookback:
            return None

        recent = volumes[-1]
        avg_volume = sum(volumes[-lookback:]) / lookback

        if avg_volume == 0:
            return None

        return recent / avg_volume

    def candle_range(self, highs: List[float], lows: List[float]):
        if not highs or not lows:
            return None

        return highs[-1] - lows[-1]

    def structure_age(self, closes: List[float], lookback: int = 20):
        if len(closes) < lookback:
            return None

        highest = max(closes[-lookback:])
        bars_since_high = lookback - 1 - closes[-lookback:].index(highest)

        return bars_since_high

    def extract(self, context) -> Dict:
        """
        Extract full measurement set.
        """

        return {
            "rsi": self.rsi_value(context.closes),
            "volume_ratio": self.volume_ratio(context.volumes),
            "candle_range": self.candle_range(context.highs, context.lows),
            "structure_age": self.structure_age(context.closes),
        }
