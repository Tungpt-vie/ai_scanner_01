from typing import Dict, List

from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.analytics.duration_analysis import DurationAnalysis
from scanner.observation.state_transition import ObservationState


class DurationService:
    """
    CLOSED observation duration analytics.
    Read-only.
    """

    def __init__(self, observation_manager: ObservationLifecycleManager):
        self.observation_manager = observation_manager

    def compute(self) -> Dict:
        observations = self.observation_manager.list_all()

        closed_observations: List[Dict] = [
            obs for obs in observations
            if obs.get("state") == ObservationState.CLOSED.value
        ]

        durations = DurationAnalysis.compute_durations(closed_observations)

        if not durations:
            return {
                "total_closed": 0,
                "avg_duration_seconds": 0,
                "min_duration_seconds": 0,
                "max_duration_seconds": 0
            }

        return {
            "total_closed": len(durations),
            "avg_duration_seconds": int(sum(durations) / len(durations)),
            "min_duration_seconds": min(durations),
            "max_duration_seconds": max(durations)
        }
