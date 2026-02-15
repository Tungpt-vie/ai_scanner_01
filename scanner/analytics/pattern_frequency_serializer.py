from typing import Dict


class PatternFrequencySerializer:
    """
    Safe serializer for Pattern Frequency Analytics.

    Rules:
    - No ranking
    - No sorting bias
    - No derived metrics
    - No winrate
    - No performance evaluation
    - Deterministic structure only
    """

    def serialize(self, data: Dict) -> Dict:
        return {
            "total_events": data.get("total_events", 0),
            "pattern_frequency": data.get("pattern_frequency", {})
        }
