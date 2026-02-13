from datetime import datetime
from scanner.observation.state_transition import ObservationState


class ObservationCloseHandler:
    """
    Explicit close controller.

    Rules:
    - CLOSED is terminal
    - No reopen
    - No escalation
    - Deterministic behavior
    """

    def close(self, record):
        """
        Close observation explicitly.
        """

        if record.state == ObservationState.CLOSED:
            raise ValueError("ALREADY_CLOSED")

        # Allow close from OPEN / UPDATED / EXPIRED
        record.state = ObservationState.CLOSED
        record.updated_at = datetime.utcnow()
