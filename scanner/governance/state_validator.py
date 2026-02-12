from scanner.governance.user_model import UserStatus


class StateValidator:
    """
    Strict lifecycle transition validator.

    Rules:
    - No illegal transitions
    - No implicit upgrade
    - No auto-recovery
    """

    ALLOWED_TRANSITIONS = {
        UserStatus.PENDING: {UserStatus.ACTIVE, UserStatus.CANCELLED},
        UserStatus.ACTIVE: {UserStatus.SUSPENDED, UserStatus.CANCELLED},
        UserStatus.SUSPENDED: {UserStatus.ACTIVE, UserStatus.CANCELLED},
        UserStatus.CANCELLED: set(),
    }

    def validate(self, current_status: UserStatus, new_status: UserStatus):
        if new_status not in self.ALLOWED_TRANSITIONS[current_status]:
            raise ValueError("INVALID_TRANSITION")
