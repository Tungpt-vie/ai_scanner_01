from datetime import datetime
from scanner.governance.user_model import User, UserStatus
from scanner.governance.user_repository import UserRepository
from scanner.governance.state_validator import StateValidator


class LifecycleManager:
    """
    Enforces validated lifecycle transitions.

    Rules:
    - All transitions must pass StateValidator
    - No silent state mutation
    - Explicit transition only
    - Audit-ready (timestamp returned)
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.validator = StateValidator()

    def transition(self, user_id: str, new_status: UserStatus) -> datetime:
        """
        Perform validated transition.
        Returns transition timestamp.
        """

        user: User = self.repository.get(user_id)

        # Validate transition
        self.validator.validate(user.status, new_status)

        # Apply transition explicitly
        user.status = new_status

        # Return audit timestamp
        return datetime.utcnow()

    def activate(self, user_id: str) -> datetime:
        return self.transition(user_id, UserStatus.ACTIVE)

    def suspend(self, user_id: str) -> datetime:
        return self.transition(user_id, UserStatus.SUSPENDED)

    def cancel(self, user_id: str) -> datetime:
        return self.transition(user_id, UserStatus.CANCELLED)
