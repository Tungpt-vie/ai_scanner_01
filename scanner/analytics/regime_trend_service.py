from typing import Dict, List
from collections import Counter

from scanner.storage.event_repository import EventRepository


class RegimeTrendService:
    """
    Read-only Regime Trend Analytics Service.

    Rules:
    - No mutation
    - No prediction
    - No ranking
    - No performance metric
    - Aggregation only
    - Deterministic output
    """

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def compute_regime_transitions(self) -> Dict:
        """
        Aggregate regime transition counts from event history.

        Assumes events may carry a regime_state attribute.
        """

        events = self.event_repository.list_all()

        regime_sequence: List[str] = []

        for event in events:
            regime = getattr(event, "regime_state", None)
            if regime:
                regime_sequence.append(regime)

        transition_counter = Counter()

        for i in range(1, len(regime_sequence)):
            prev_regime = regime_sequence[i - 1]
            current_regime = regime_sequence[i]
            transition_key = f"{prev_regime}→{current_regime}"
            transition_counter[transition_key] += 1

        return {
            "total_regime_events": len(regime_sequence),
            "transition_frequency": dict(transition_counter)
        }
