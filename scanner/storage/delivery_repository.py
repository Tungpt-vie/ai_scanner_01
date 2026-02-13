from datetime import datetime
from typing import Dict, Tuple


class DeliveryRecord:
    """
    Delivery record per (event_hash, user_id).

    Rules:
    - Immutable once stored
    - No escalation
    - No replay mutation
    """

    def __init__(self, event_hash: str, user_id: str):
        self.event_hash = event_hash
        self.user_id = user_id
        self.delivered_at = datetime.utcnow()

    def to_dict(self):
        return {
            "event_hash": self.event_hash,
            "user_id": self.user_id,
            "delivered_at": self.delivered_at.isoformat(),
        }


class DeliveryRepository:
    """
    In-memory delivery tracking repository.

    Rules:
    - Idempotent storage
    - No duplicate delivery record
    - No replay logic
    - TTL handled externally
    """

    def __init__(self):
        # Keyed by (event_hash, user_id)
        self._deliveries: Dict[Tuple[str, str], DeliveryRecord] = {}

    def mark_delivered(self, event_hash: str, user_id: str):
        key = (event_hash, user_id)

        if key in self._deliveries:
            return  # idempotent, do nothing

        record = DeliveryRecord(event_hash, user_id)
        self._deliveries[key] = record

    def has_delivered(self, event_hash: str, user_id: str) -> bool:
        return (event_hash, user_id) in self._deliveries

    def get(self, event_hash: str, user_id: str) -> DeliveryRecord:
        key = (event_hash, user_id)

        if key not in self._deliveries:
            raise ValueError("DELIVERY_NOT_FOUND")

        return self._deliveries[key]

    def delete(self, event_hash: str, user_id: str):
        key = (event_hash, user_id)

        if key not in self._deliveries:
            raise ValueError("DELIVERY_NOT_FOUND")

        del self._deliveries[key]

    def list_all(self):
        return [
            record.to_dict()
            for record in self._deliveries.values()
        ]
