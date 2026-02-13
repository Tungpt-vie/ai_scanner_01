from datetime import datetime, timedelta
from typing import Dict, Tuple


class CooldownManager:
    """
    Deterministic cooldown & idempotency control.

    Rules:
    - Prevent duplicate delivery within cooldown window
    - No randomness
    - No background thread
    - Pure in-memory control
    - Keyed by (user_id, symbol)
    """

    def __init__(self, cooldown_seconds: int = 300):
        """
        cooldown_seconds default: 5 minutes
        """
        self.cooldown_seconds = cooldown_seconds
        self._last_delivery: Dict[Tuple[str, str], datetime] = {}

    def can_deliver(self, user_id: str, symbol: str) -> bool:
        """
        Check if delivery allowed based on cooldown.
        """

        key = (user_id, symbol)

        if key not in self._last_delivery:
            return True

        last_time = self._last_delivery[key]
        now = datetime.utcnow()

        if now - last_time >= timedelta(seconds=self.cooldown_seconds):
            return True

        return False

    def mark_delivered(self, user_id: str, symbol: str):
        """
        Mark delivery timestamp.
        """
        key = (user_id, symbol)
        self._last_delivery[key] = datetime.utcnow()

    def reset(self):
        """
        Clear cooldown state.
        """
        self._last_delivery.clear()
