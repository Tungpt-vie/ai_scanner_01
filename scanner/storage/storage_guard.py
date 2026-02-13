from typing import Dict
from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository


class StorageGuard:
    """
    Storage boundary enforcement layer.

    Responsibilities:
    - Prevent duplicate event storage
    - Prevent duplicate delivery marking
    - No replay logic
    - No scanner mutation
    - Deterministic behavior
    """

    def __init__(
        self,
        event_repo: EventRepository,
        delivery_repo: DeliveryRepository,
    ):
        self.event_repo = event_repo
        self.delivery_repo = delivery_repo

    def store_event(self, payload: Dict) -> str:
        """
        Store event safely (idempotent).
        Returns event_hash.
        """
        return self.event_repo.store(payload)

    def mark_delivery(self, event_hash: str, user_id: str):
        """
        Mark delivery if not already recorded.
        """
        self.delivery_repo.mark_delivered(event_hash, user_id)

    def has_been_delivered(self, event_hash: str, user_id: str) -> bool:
        return self.delivery_repo.has_delivered(event_hash, user_id)
