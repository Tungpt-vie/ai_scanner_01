from datetime import datetime, timedelta
from scanner.observation.state_transition import ObservationState


class ObservationExpiryHandler:
    """
    Handles time-based expiration of observations.

    Rules:
    - No reopen once expired
    - No escalation
    - Deterministic expiry window
    - No background scheduler (manual invocation only)
    """

    def __init__(self, expiry_minutes: int = 60):
        """
        Default expiry window: 60 minutes
        """
        self.expiry_minutes = expiry_minutes

    def should_expire(self, created_at: datetime) -> bool:
        """
        Determine if observation should expire.
        """

        now = datetime.utcnow()
        return now - created_at >= timedelta(minutes=self.expiry_minutes)

    def apply_expiry(self, record):
        """
        Apply EXPIRED state if eligible.
        """

        if record.state == ObservationState.CLOSED:
            return  # no reopen

        if record.state in (ObservationState.OPEN, ObservationState.UPDATED):
            if self.should_expire(record.created_at):
                record.state = ObservationState.EXPIRED
                record.updated_at = datetime.utcnow()
