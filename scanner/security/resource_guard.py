from typing import Dict


class ResourceGuard:
    """
    Resource protection layer.

    Rules:
    - Limit number of in-memory objects
    - No silent overflow
    - Deterministic enforcement
    - No scanner mutation
    """

    def __init__(
        self,
        max_events: int = 10000,
        max_deliveries: int = 50000,
        max_observations: int = 10000,
    ):
        self.max_events = max_events
        self.max_deliveries = max_deliveries
        self.max_observations = max_observations

    def check_event_capacity(self, current_count: int):
        if current_count > self.max_events:
            raise MemoryError("EVENT_CAPACITY_EXCEEDED")

    def check_delivery_capacity(self, current_count: int):
        if current_count > self.max_deliveries:
            raise MemoryError("DELIVERY_CAPACITY_EXCEEDED")

    def check_observation_capacity(self, current_count: int):
        if current_count > self.max_observations:
            raise MemoryError("OBSERVATION_CAPACITY_EXCEEDED")

    def validate_all(
        self,
        counts: Dict[str, int],
    ):
        """
        counts example:
        {
            "events": 100,
            "deliveries": 200,
            "observations": 50
        }
        """

        if "events" in counts:
            self.check_event_capacity(counts["events"])

        if "deliveries" in counts:
            self.check_delivery_capacity(counts["deliveries"])

        if "observations" in counts:
            self.check_observation_capacity(counts["observations"])
