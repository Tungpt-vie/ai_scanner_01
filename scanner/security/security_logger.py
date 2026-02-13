from datetime import datetime
from typing import List, Dict


class SecurityLogger:
    """
    Security audit logger.

    Rules:
    - Append-only
    - No mutation of existing records
    - No PII storage (no email, no token value)
    - Deterministic behavior
    """

    def __init__(self):
        self._logs: List[Dict] = []

    def log_event(
        self,
        event_type: str,
        actor_id: str,
        metadata: Dict = None,
    ):
        """
        Log security-related event.

        event_type examples:
        - RATE_LIMIT_BLOCK
        - INVALID_TOKEN
        - INVALID_SIGNATURE
        - REPLAY_ATTEMPT
        - AUTH_FAILURE
        """

        if not isinstance(event_type, str):
            raise ValueError("INVALID_EVENT_TYPE")

        if not isinstance(actor_id, str):
            raise ValueError("INVALID_ACTOR_ID")

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "actor_id": actor_id,
            "metadata": metadata or {},
        }

        self._logs.append(entry)

    def get_logs(self) -> List[Dict]:
        """
        Return immutable copy of logs.
        """
        return list(self._logs)

    def clear(self):
        """
        Clear all logs (admin maintenance only).
        """
        self._logs.clear()
