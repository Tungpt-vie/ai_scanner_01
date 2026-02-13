from enum import Enum


class ObservationState(Enum):
    """
    Observation lifecycle states.

    Rules:
    - No escalation to STANDARD
    - No reopen once CLOSED
    """

    OPEN = "OPEN"
    UPDATED = "UPDATED"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"


class ObservationStateTransition:
    """
    Strict state transition controller.

    Allowed transitions:
    OPEN → UPDATED
    OPEN → EXPIRED
    OPEN → CLOSED
    UPDATED → EXPIRED
    UPDATED → CLOSED
    EXPIRED → CLOSED

    Forbidden:
    - CLOSED → any
    - Any → OPEN
    - Any escalation outside observation domain
    """

    ALLOWED_TRANSITIONS = {
        ObservationState.OPEN: {
            ObservationState.UPDATED,
            ObservationState.EXPIRED,
            ObservationState.CLOSED,
        },
        ObservationState.UPDATED: {
            ObservationState.EXPIRED,
            ObservationState.CLOSED,
        },
        ObservationState.EXPIRED: {
            ObservationState.CLOSED,
        },
        ObservationState.CLOSED: set(),
    }

    def validate(self, current_state: ObservationState, new_state: ObservationState):
        if new_state not in self.ALLOWED_TRANSITIONS[current_state]:
            raise ValueError("INVALID_OBSERVATION_TRANSITION")
