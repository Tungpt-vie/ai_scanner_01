from typing import Dict
from scanner.optimization.regime_cache import RegimeCache


class MarketRegimeService:
    """
    Read-only Market Regime Snapshot Service.

    Uses cached regime state.
    Does NOT recompute.
    """

    def __init__(self, regime_cache: RegimeCache):
        self.regime_cache = regime_cache

    def get_current_regime(self) -> Dict:
        """
        Return last cached regime snapshot.
        """

        # Access internal cached state safely
        regime = getattr(self.regime_cache, "current_regime", None)

        if regime is None:
            regime = "UNKNOWN"

        return {
            "regime": regime,
            "source": "REGIME_CACHE",
        }

    def get_regime_metadata(self):
        return None
