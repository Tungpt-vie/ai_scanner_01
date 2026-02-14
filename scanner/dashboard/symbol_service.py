from typing import Optional, Dict, List
from scanner.storage.event_repository import EventRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager


class SymbolStateService:
    """
    Read-only symbol snapshot aggregation service.

    Rules:
    - No scan trigger
    - No mutation
    - No event rewrite
    - Snapshot view only
    """

    def __init__(
        self,
        event_repo: EventRepository,
        observation_manager: ObservationLifecycleManager,
    ):
        self.event_repo = event_repo
        self.observation_manager = observation_manager

    def get_symbol_state(self, symbol: str) -> Dict:
        """
        Build snapshot state for a symbol.
        """

        events = self._get_events_for_symbol(symbol)
        observations = self._get_observations_for_symbol(symbol)

        latest_event = events[0] if events else None

        return {
            "symbol": symbol,
            "event_count": len(events),
            "latest_event": latest_event,
            "observation_count": len(observations),
            "observations": observations,
        }

    # ----------------------------
    # INTERNAL HELPERS
    # ----------------------------

    def _get_events_for_symbol(self, symbol: str) -> List[Dict]:
        all_events = self.event_repo.list_all()

        filtered = [
            e for e in all_events
            if e.get("payload", {}).get("symbol") == symbol
        ]

        # Immutable sort by created_at (descending)
        filtered.sort(
            key=lambda e: e["created_at"],
            reverse=True,
        )

        return filtered

    def _get_observations_for_symbol(self, symbol: str) -> List[Dict]:
        all_observations = self.observation_manager.list_all()

        # ObservationRecord currently does not bind symbol,
        # so snapshot returns all for now (future extension).
        # Still read-only and deterministic.
        return all_observations
