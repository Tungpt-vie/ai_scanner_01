from typing import List, Dict, Optional
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.observation.state_transition import ObservationState


class ObservationHistoryService:
    """
    Read-only history query service.

    Rules:
    - CLOSED observations only
    - Immutable ordering
    - No reopen
    - No mutation
    - No scan trigger
    """

    def __init__(self, observation_manager: ObservationLifecycleManager):
        self.observation_manager = observation_manager

    def get_closed_history(
        self,
        descending: bool = True,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        """
        Return CLOSED observation history.
        """

        all_observations = self.observation_manager.list_all()

        closed = [
            obs for obs in all_observations
            if obs.get("state") == ObservationState.CLOSED.value
        ]

        # Immutable sort by updated_at (CLOSED timestamp)
        closed.sort(
            key=lambda o: o.get("updated_at"),
            reverse=descending,
        )

        if limit:
            closed = closed[:limit]

        return closed
