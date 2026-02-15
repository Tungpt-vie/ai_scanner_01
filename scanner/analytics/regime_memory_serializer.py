from typing import Dict


class RegimeMemorySerializer:
    """
    Safe Regime Memory output.
    No prediction.
    No ranking.
    Deterministic.
    """

    def serialize(self, data: Dict) -> Dict:
        return {
            "total_regime_points": data.get("total_regime_points", 0),
            "max_streak_per_regime": data.get("max_streak_per_regime", {})
        }
