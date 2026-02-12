from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class UserStatus(Enum):
    """
    Strict lifecycle states.
    """

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


@dataclass
class User:
    """
    Governance user model.

    Rules:
    - Default status must be PENDING
    - No auto-approval
    - No implicit upgrade
    """

    user_id: str
    email: str
    created_at: datetime
    status: UserStatus = UserStatus.PENDING

    def activate(self):
        if self.status != UserStatus.PENDING:
            raise ValueError("INVALID_TRANSITION")
        self.status = UserStatus.ACTIVE

    def suspend(self):
        if self.status != UserStatus.ACTIVE:
            raise ValueError("INVALID_TRANSITION")
        self.status = UserStatus.SUSPENDED

    def cancel(self):
        if self.status not in [UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.SUSPENDED]:
            raise ValueError("INVALID_TRANSITION")
        self.status = UserStatus.CANCELLED
