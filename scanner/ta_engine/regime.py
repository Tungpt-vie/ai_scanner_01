
from enum import Enum
from typing import List
from statistics import stdev


class MarketRegime(Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    VOLATILE = "VOLATILE"
    COMPRESSION = "COMPRESSION"
    UNKNOWN = "UNKNOWN"


class RegimeDetector:
    """
    Deterministic market regime classification.
    No prediction, no randomness.
    """

    def __init__(self, lookback: int = 20):
        self.lookback = lookback

    def detect(self, closes: List[float]) -> MarketRegime:

        if len(closes) < self.lookback:
            return MarketRegime.UNKNOWN

        window = closes[-self.lookback:]

        price_range = max(window) - min(window)
        mean_price = sum(window) / len(window)

        if mean_price == 0:
            return MarketRegime.UNKNOWN

        volatility_ratio = price_range / mean_price

        # Volatile market
        if volatility_ratio > 0.08:
            return MarketRegime.VOLATILE

        # Compression (very tight range)
        if volatility_ratio < 0.01:
            return MarketRegime.COMPRESSION

        # Trend detection (simple slope logic)
        slope = window[-1] - window[0]

        if abs(slope) > (0.03 * mean_price):
            return MarketRegime.TRENDING

        return MarketRegime.RANGING
