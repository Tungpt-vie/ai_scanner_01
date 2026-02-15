from typing import Dict


class DurationSerializer:
    """
    Safe deterministic output.
    No profit.
    No winrate.
    No ranking.
    """

    def serialize(self, data: Dict) -> Dict:
        return {
            "total_closed": data.get("total_closed", 0),
            "avg_duration_seconds": data.get("avg_duration_seconds", 0),
            "min_duration_seconds": data.get("min_duration_seconds", 0),
            "max_duration_seconds": data.get("max_duration_seconds", 0),
        }
