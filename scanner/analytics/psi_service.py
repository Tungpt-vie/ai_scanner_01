from typing import Dict

from scanner.storage.event_repository import EventRepository
from scanner.analytics.psi_calculator import PSICalculator


class PSIService:
    """
    Pattern Stability Index Service.
    Read-only.
    """

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def compute(self) -> Dict:
        events = self.event_repository.list_all()

        pattern_frequency: Dict[str, int] = {}

        for event in events:
            pattern = getattr(event, "event_type", None)
            if not pattern:
                continue

            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1

        psi_scores = PSICalculator.compute(pattern_frequency)

        return {
            "total_events": len(events),
            "psi_scores": psi_scores
        }
