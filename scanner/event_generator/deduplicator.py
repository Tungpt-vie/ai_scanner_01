from typing import Dict, Tuple
from scanner.event_generator.schema import TAEvent


class EventDeduplicator:
    """
    Prevent duplicate TAEvent emissions.

    Dedup key:
    (symbol, regime, ta_state, filter_state)
    """

    def __init__(self):
        self._seen: Dict[Tuple[str, str, str, str], float] = {}

    def is_duplicate(self, event: TAEvent) -> bool:
        """
        Return True if event already emitted with same structural identity.
        """

        key = (
            event.symbol,
            event.regime,
            event.ta_state,
            event.filter_state,
        )

        if key in self._seen:
            return True

        # Store confidence as reference (optional state memory)
        self._seen[key] = event.confidence
        return False

    def reset(self):
        """
        Clear dedup memory (e.g., new trading day).
        """
        self._seen.clear()
