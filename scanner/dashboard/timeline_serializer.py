from typing import List, Dict


class TimelineSerializer:
    """
    Safe serializer for timeline view.

    Rules:
    - No raw payload exposure
    - No internal repository fields
    - No PII
    - Read-only transformation
    """

    def serialize_event(self, event: Dict) -> Dict:
        """
        Return safe timeline event view.
        """

        payload = event.get("payload", {})

        return {
            "event_hash": event.get("event_hash"),
            "created_at": event.get("created_at"),
            "symbol": payload.get("symbol"),
            "type": payload.get("type"),
        }

    def serialize_list(self, events: List[Dict]) -> List[Dict]:
        return [self.serialize_event(e) for e in events]
