from scanner.governance.user_model import UserStatus
from scanner.governance.user_repository import UserRepository


class DeliveryGuard:
    """
    Output delivery gate.

    Rules:
    - Only ACTIVE users receive output
    - PENDING / SUSPENDED / CANCELLED are hard blocked
    - No soft allowance
    - Deterministic behavior
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def allow_delivery(self, user_id: str) -> bool:
        """
        Return True if user is ACTIVE.
        """

        user = self.repository.get(user_id)

        if user.status == UserStatus.ACTIVE:
            return True

        return False
