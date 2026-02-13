from datetime import datetime, timedelta
from typing import Dict, List


class RateLimiter:
    """
    Deterministic rate limiter.

    Rules:
    - Per-key limit (user/admin/IP)
    - Fixed time window
    - No randomness
    - No background thread
    - In-memory only
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        max_requests: allowed within window
        window_seconds: time window size
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[datetime]] = {}

    def allow(self, key: str) -> bool:
        """
        Returns True if request allowed.
        """

        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)

        if key not in self._requests:
            self._requests[key] = []

        # Remove expired timestamps
        self._requests[key] = [
            ts for ts in self._requests[key]
            if ts >= window_start
        ]

        if len(self._requests[key]) >= self.max_requests:
            return False

        self._requests[key].append(now)
        return True

    def reset(self, key: str = None):
        """
        Reset rate limit state.
        """
        if key:
            self._requests.pop(key, None)
        else:
            self._requests.clear()
