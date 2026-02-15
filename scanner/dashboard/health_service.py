import time
from typing import Dict

from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.optimization.regime_cache import RegimeCache


class SystemHealthService:
    """
    Read-only system health aggregation service.

    Rules:
    - No mutation
    - No scan trigger
    - No recompute
    - Deterministic snapshot
    """

    def __init__(
        self,
        event_repo: EventRepository,
        delivery_repo: DeliveryRepository,
        observation_manager: ObservationLifecycleManager,
        regime_cache: RegimeCache,
    ):
        self.event_repo = event_repo
        self.delivery_repo = delivery_repo
        self.observation_manager = observation_manager
        self.regime_cache = regime_cache

        # Capture server start time once
        self.start_time = time.time()

    def get_health_snapshot(self) -> Dict:
        """
        Return deterministic system health snapshot.
        """

        total_events = len(self.event_repo.list_all())
        total_deliveries = len(self.delivery_repo.list_all())
        total_observations = len(self.observation_manager.list_all())

        current_regime = getattr(self.regime_cache, "current_regime", "UNKNOWN")

        uptime_seconds = int(time.time() - self.start_time)

        return {
            "total_events": total_events,
            "total_deliveries": total_deliveries,
            "total_observations": total_observations,
            "current_regime": current_regime,
            "uptime_seconds": uptime_seconds,
        }
