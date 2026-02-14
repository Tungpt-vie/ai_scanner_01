from typing import List, Optional, Dict
from datetime import datetime

from scanner.storage.event_repository import EventRepository


class TimelineService:
    """
    Immutable timeline query layer.

    Rules:
    - Read-only
    - No mutation
    - No backfill
    - No reorder
    - Sort strictly by created_at (ascending or descending)
    """

    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def get_timeline(
        self,
        symbol: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        descending: bool = True,
    ) -> List[Dict]:
        """
        Query timeline with optional filters.
        """

        events = self.event_repo.list_all()

        filtered = []

        for event in events:
            created_at = datetime.fromisoformat(event["created_at"])

            # Symbol filter
            if symbol:
                payload_symbol = event.get("payload", {}).get("symbol")
                if payload_symbol != symbol:
                    continue

            # Start time filter
            if start_time and created_at < start_time:
                continue

            # End time filter
            if end_time and created_at > end_time:
                continue

            filtered.append(event)

        # Immutable ordering by created_at
        filtered.sort(
            key=lambda e: e["created_at"],
            reverse=descending,
        )

        return filtered
