from typing import Dict
from collections import Counter

from scanner.storage.event_repository import EventRepository


class PatternFrequencyService:
    """
    Read-only Pattern Frequency Analytics Service.

    Rules:
    - No mutation
    - No event modification
    - No ranking
    - No performance metrics
    - Deterministic aggregation only
    """

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def compute_frequency(self) -> Dict:
        """
        Aggregate frequency of event types.
        """

        events = self.event_repository.list_all()

        pattern_counter = Counter()

        for event in events:
            event_type = getattr(event, "event_type", None)
            if event_type:
                pattern_counter[event_type] += 1

        total_events = len(events)

        return {
            "total_events": total_events,
            "pattern_frequency": dict(pattern_counter)
        }
