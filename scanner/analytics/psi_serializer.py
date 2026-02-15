from typing import Dict


class PSISerializer:
    """
    Safe PSI output.
    No ranking.
    No interpretation.
    Deterministic.
    """

    def serialize(self, data: Dict) -> Dict:
        return {
            "total_events": data.get("total_events", 0),
            "psi_scores": data.get("psi_scores", {})
        }
