from scanner.ops.state_snapshot import StateSnapshot
from scanner.ops.recovery_guard import RecoveryGuard


class ResumeManager:
    """
    Coordinates safe restart behavior.

    Responsibilities:
    - Hold snapshot reference
    - Apply recovery guard rules
    - Ensure no replay / no backfill
    - Resume in silent mode
    """

    def __init__(self):
        self.snapshot = StateSnapshot()
        self.guard = RecoveryGuard()
        self._resume_mode = False

    def capture_state(
        self,
        last_symbol: str,
        last_regime: str,
        last_filter_state: str,
        session_active: bool,
    ):
        """
        Capture structural runtime state.
        """
        self.snapshot.capture(
            last_symbol=last_symbol,
            last_regime=last_regime,
            last_filter_state=last_filter_state,
            session_active=session_active,
        )

    def attempt_resume(self) -> bool:
        """
        Attempt safe resume.
        Always silent.
        """

        state = self.snapshot.get_state()

        allowed = self.guard.allow_resume(state)

        self._resume_mode = True
        return allowed

    def in_resume_mode(self) -> bool:
        """
        Check if system is currently in resume mode.
        """
        return self._resume_mode

    def reset(self):
        """
        Hard reset system state.
        """
        self.snapshot.clear()
        self._resume_mode = False
