from typing import Dict


class SystemHealthSerializer:
    """
    Safe serializer for System Health endpoint.

    Rules:
    - No internal repository exposure
    - No object references
    - Deterministic structure
    """

    def serialize(self, health_data: Dict) -> Dict:
        return {
            "total_events": health_data.get("total_events", 0),
            "total_deliveries": health_data.get("total_deliveries", 0),
            "total_observations": health_data.get("total_observations", 0),
            "current_regime": health_data.get("current_regime", "UNKNOWN"),
            "uptime_seconds": health_data.get("uptime_seconds", 0),
        }
