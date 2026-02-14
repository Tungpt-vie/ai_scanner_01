from typing import List, Dict
from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager


class DashboardQueryService:
    """
    Read-only dashboard query layer.

    Rules:
    - No mutation
    - No scanner trigger
    - No write access
    - Aggregation only
    """

    def __init__(
        self,
        event_repo: EventRepository,
        delivery_repo: DeliveryRepository,
        observation_manager: ObservationLifecycleManager,
    ):
        self.event_repo = event_repo
        self.delivery_repo = delivery_repo
        self.observation_manager = observation_manager

    # ---------------------------
    # EVENTS
    # ---------------------------

    def list_events(self) -> List[Dict]:
        """
        Return all stored events.
        """
        return self.event_repo.list_all()

    def event_count(self) -> int:
        return len(self.event_repo.list_all())

    # ---------------------------
    # DELIVERIES
    # ---------------------------

    def list_deliveries(self) -> List[Dict]:
        return self.delivery_repo.list_all()

    def delivery_count(self) -> int:
        return len(self.delivery_repo.list_all())

    # ---------------------------
    # OBSERVATIONS
    # ---------------------------

    def list_observations(self) -> List[Dict]:
        return self.observation_manager.list_all()

    def observation_count(self) -> int:
        return len(self.observation_manager.list_all())

    # ---------------------------
    # SUMMARY
    # ---------------------------

    def summary(self) -> Dict:
        """
        Aggregate high-level system snapshot.
        """

        return {
            "events": self.event_count(),
            "deliveries": self.delivery_count(),
            "observations": self.observation_count(),
        }
