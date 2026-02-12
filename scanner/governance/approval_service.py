from datetime import datetime
from scanner.governance.admin_repository import AdminRepository
from scanner.governance.user_repository import UserRepository
from scanner.governance.user_model import UserStatus
from scanner.governance.audit_logger import AuditLogger


class ApprovalService:
    """
    Explicit admin approval service.

    Rules:
    - No auto-approve
    - Admin role must allow approval
    - All actions logged
    - No direct mutation without validation
    """

    def __init__(
        self,
        admin_repo: AdminRepository,
        user_repo: UserRepository,
        audit_logger: AuditLogger,
    ):
        self.admin_repo = admin_repo
        self.user_repo = user_repo
        self.audit_logger = audit_logger

    def approve_user(self, admin_id: str, user_id: str) -> datetime:
        admin = self.admin_repo.get(admin_id)

        if not admin.can_approve():
            raise PermissionError("ADMIN_NOT_AUTHORIZED")

        user = self.user_repo.get(user_id)

        if user.status != UserStatus.PENDING:
            raise ValueError("USER_NOT_PENDING")

        old_status = user.status
        user.status = UserStatus.ACTIVE
        timestamp = datetime.utcnow()

        self.audit_logger.log_transition(
            user_id=user.user_id,
            from_status=old_status,
            to_status=user.status,
            timestamp=timestamp,
        )

        return timestamp

    def ban_user(self, admin_id: str, user_id: str) -> datetime:
        admin = self.admin_repo.get(admin_id)

        if not admin.can_ban():
            raise PermissionError("ADMIN_NOT_AUTHORIZED")

        user = self.user_repo.get(user_id)

        old_status = user.status
        user.status = UserStatus.CANCELLED
        timestamp = datetime.utcnow()

        self.audit_logger.log_transition(
            user_id=user.user_id,
            from_status=old_status,
            to_status=user.status,
            timestamp=timestamp,
        )

        return timestamp
