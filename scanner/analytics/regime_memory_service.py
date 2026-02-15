from typing import Dict, List

from scanner.storage.event_repository import EventRepository


class RegimeMemoryService:
    """
    Regime Memory Analytics.

    Measures consecutive regime streak lengths.
    Read-only.
    Deterministic.
    """

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def compute(self) -> Dict:
        events = self.event_repository.list_all()

        regime_sequence: List[str] = []

        for event in events:
            regime = getattr(event, "regime_state", None)
            if regime:
                regime_sequence.append(regime)

        if not regime_sequence:
            return {
                "total_regime_points": 0,
                "max_streak_per_regime": {}
            }

        max_streak: Dict[str, int] = {}
        current_regime = regime_sequence[0]
        current_streak = 1

        for regime in regime_sequence[1:]:
            if regime == current_regime:
                current_streak += 1
            else:
                max_streak[current_regime] = max(
                    max_streak.get(current_regime, 0),
                    current_streak
                )
                current_regime = regime
                current_streak = 1

        # finalize last streak
        max_streak[current_regime] = max(
            max_streak.get(current_regime, 0),
            current_streak
        )

        return {
            "total_regime_points": len(regime_sequence),
            "max_streak_per_regime": max_streak
        }
