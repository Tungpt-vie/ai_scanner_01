from typing import Dict, List


class SymbolStateSerializer:
    """
    Safe serializer for Symbol State Card.

    Rules:
    - No raw payload exposure
    - No internal storage fields
    - No PII
    - Snapshot view only
    """

    def serialize(self, state: Dict) -> Dict:
        latest_event = state.get("latest_event")

        return {
            "symbol": state.get("symbol"),
            "event_count": state.get("event_count", 0),
            "latest_event": self._serialize_event(latest_event)
            if latest_event else None,
            "observation_count": state.get("observation_count", 0),
        }

    # ----------------------------
    # INTERNAL HELPERS
    # ----------------------------

    def _serialize_event(self, event: Dict) -> Dict:
        payload = event.get("payload", {})

        return {
            "event_hash": event.get("event_hash"),
            "created_at": event.get("created_at"),
            "symbol": payload.get("symbol"),
            "type": payload.get("type"),
        }
