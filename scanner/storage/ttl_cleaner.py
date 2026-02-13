from datetime import datetime, timedelta
from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository


class TTLCleaner:
    """
    Time-based cleanup controller.

    Rules:
    - Deterministic cleanup
    - No replay resurrection
    - No auto reprocessing
    - Manual invocation only
    """

    def __init__(
        self,
        event_repo: EventRepository,
        delivery_repo: DeliveryRepository,
        ttl_minutes: int = 60,
    ):
        self.event_repo = event_repo
        self.delivery_repo = delivery_repo
        self.ttl_minutes = ttl_minutes

    def clean_expired_events(self):
        """
        Remove expired events and their delivery records.
        """

        now = datetime.utcnow()
        expiry_delta = timedelta(minutes=self.ttl_minutes)

        expired_hashes = []

        for record in self.event_repo._events.values():
            if now - record.created_at >= expiry_delta:
                expired_hashes.append(record.event_hash)

        # Delete expired events
        for event_hash in expired_hashes:
            self.event_repo.delete(event_hash)

        # Delete associated delivery records
        for key in list(self.delivery_repo._deliveries.keys()):
            event_hash, user_id = key
            if event_hash in expired_hashes:
                self.delivery_repo.delete(event_hash, user_id)
