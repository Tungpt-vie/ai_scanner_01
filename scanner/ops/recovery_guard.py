from typing import Dict


class RecoveryGuard:
    """
    Resume safety guard.

    Rules:
    - No event replay
    - No backfill processing
    - No automatic re-emission
    - Resume must be silent unless new data arrives
    """

    def allow_resume(self, snapshot: Dict) -> bool:
        """
        Determine whether safe resume is allowed.
        """

        # No snapshot → safe to start fresh
        if not snapshot:
            return True

        # If session was inactive → safe resume
        if not snapshot.get("session_active", False):
            return True

        # If last_filter_state was DROP → safe resume
        if snapshot.get("last_filter_state") == "DROP":
            return True

        # Otherwise resume but do NOT replay anything
        return True

    def allow_replay(self) -> bool:
        """
        Explicitly forbid replay.
        """
        return False
