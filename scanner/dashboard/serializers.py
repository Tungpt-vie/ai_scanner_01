from typing import Dict, List


class DashboardSerializer:
    """
    Safe serializer layer for dashboard responses.

    Rules:
    - No internal object exposure
    - No raw repository reference
    - No PII
    - Read-only transformation
    """

    # ---------------------------
    # EVENTS
    # ---------------------------

    def serialize_event(self, event: Dict) -> Dict:
        """
        Return safe event view.
        """

        return {
            "event_hash": event.get("event_hash"),
            "created_at": event.get("created_at"),
            "symbol": event.get("payload", {}).get("symbol"),
            "type": event.get("payload", {}).get("type"),
        }

    def serialize_event_list(self, events: List[Dict]) -> List[Dict]:
        return [self.serialize_event(e) for e in events]

    # ---------------------------
    # DELIVERIES
    # ---------------------------

    def serialize_delivery(self, delivery: Dict) -> Dict:
        return {
            "event_hash": delivery.get("event_hash"),
            "user_id": delivery.get("user_id"),
            "delivered_at": delivery.get("delivered_at"),
        }

    def serialize_delivery_list(self, deliveries: List[Dict]) -> List[Dict]:
        return [self.serialize_delivery(d) for d in deliveries]

    # ---------------------------
    # OBSERVATIONS
    # ---------------------------

    def serialize_observation(self, observation: Dict) -> Dict:
        return {
            "observation_id": observation.get("observation_id"),
            "state": observation.get("state"),
            "created_at": observation.get("created_at"),
            "updated_at": observation.get("updated_at"),
        }

    def serialize_observation_list(self, observations: List[Dict]) -> List[Dict]:
        return [self.serialize_observation(o) for o in observations]

    # ---------------------------
    # SUMMARY
    # ---------------------------

    def serialize_summary(self, summary: Dict) -> Dict:
        return {
            "events": summary.get("events", 0),
            "deliveries": summary.get("deliveries", 0),
            "observations": summary.get("observations", 0),
        }
