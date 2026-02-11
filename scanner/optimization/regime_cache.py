from scanner.optimization.cache_store import SimpleCacheStore
from scanner.ta_engine.regime import RegimeDetector, MarketRegime


class RegimeCache:
    """
    Regime caching layer.

    Purpose:
    - Avoid recalculating regime if unchanged
    - Deterministic behavior
    - No override of logic
    """

    def __init__(self):
        self.cache = SimpleCacheStore()
        self.detector = RegimeDetector()

    def get_regime(self, symbol: str, closes) -> MarketRegime:
        """
        Return cached regime if unchanged,
        otherwise recalculate and update cache.
        """

        new_regime = self.detector.detect(closes)

        cached_regime = self.cache.get(symbol)

        if cached_regime == new_regime.value:
            return new_regime

        # Update cache
        self.cache.set(symbol, new_regime.value)
        return new_regime

    def reset(self):
        """
        Clear regime cache (e.g., new trading day).
        """
        self.cache.clear()
