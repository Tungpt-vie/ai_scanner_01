from typing import Dict


class RegimeTrendSerializer:
    """
    Safe serializer for Regime Trend Analytics.

    Rules:
    - No prediction
    - No derived metrics
    - No ranking
    - No bias interpretation
    - Deterministic structure only
    """

    def serialize(self, data: Dict) -> Dict:
        return {
            "total_regime_events": data.get("total_regime_events", 0),
            "transition_frequency": data.get("transition_frequency", {})
        }
