from datetime import datetime
from typing import List, Dict
from scanner.governance.user_model import UserStatus


class AuditLogger:
    """
    Immutable lifecycle audit logger.

    Rules:
    - Log only lifecycle transitions
    - No mutation of user object
    - Append-only
    - No deletion
    """

    def __init__(self):
        self._logs: List[Dict] = []

    def log_transition(
        self,
        user_id: str,
        from_status: UserStatus,
        to_status: UserStatus,
        timestamp: datetime,
    ):
        entry = {
            "user_id": user_id,
            "from": from_status.value,
            "to": to_status.value,
            "timestamp": timestamp.isoformat(),
        }

        self._logs.append(entry)

    def get_logs(self) -> List[Dict]:
        return list(self._logs)
