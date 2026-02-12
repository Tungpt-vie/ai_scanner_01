from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class AdminRole(Enum):
    """
    Strict admin roles.
    """

    SUPER_ADMIN = "SUPER_ADMIN"
    OPERATOR = "OPERATOR"
    AUDITOR = "AUDITOR"


@dataclass(frozen=True)
class Admin:
    """
    Immutable Admin entity.

    Rules:
    - Role is immutable
    - No implicit privilege escalation
    - No direct scanner logic access
    """

    admin_id: str
    email: str
    role: AdminRole
    created_at: datetime

    def can_approve(self) -> bool:
        return self.role in {AdminRole.SUPER_ADMIN, AdminRole.OPERATOR}

    def can_ban(self) -> bool:
        return self.role == AdminRole.SUPER_ADMIN

    def can_view_audit(self) -> bool:
        return self.role in {AdminRole.SUPER_ADMIN, AdminRole.AUDITOR}
