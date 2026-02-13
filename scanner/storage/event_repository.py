from datetime import datetime
from typing import Dict

from scanner.storage.hash_generator import EventHashGenerator


class EventRecord:
    """
    Stored event record (in-memory).

    Rules:
    - Immutable payload
    - Timestamped
    - Hash-identified
    """

    def __init__(self, payload: Dict, event_hash: str):
        self.payload = payload
        self.event_hash = event_hash
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "event_hash": self.event_hash,
            "created_at": self.created_at.isoformat(),
            "payload": self.payload,
        }


class EventRepository:
    """
    In-memory event storage.

    Rules:
    - Dedup enforced by hash
    - No replay logic
    - No mutation
    - TTL handled externally
    """

    def __init__(self):
        self._events: Dict[str, EventRecord] = {}
        self._hasher = EventHashGenerator()

    def store(self, payload: Dict) -> str:
        """
        Store event if not already stored.
        Returns event_hash.
        """

        event_hash = self._hasher.generate(payload)

        if event_hash in self._events:
            return event_hash  # idempotent

        record = EventRecord(payload, event_hash)
        self._events[event_hash] = record

        return event_hash

    def exists(self, event_hash: str) -> bool:
        return event_hash in self._events

    def get(self, event_hash: str) -> EventRecord:
        if event_hash not in self._events:
            raise ValueError("EVENT_NOT_FOUND")
        return self._events[event_hash]

    def delete(self, event_hash: str):
        if event_hash not in self._events:
            raise ValueError("EVENT_NOT_FOUND")
        del self._events[event_hash]

    def list_all(self):
        return [record.to_dict() for record in self._events.values()]
