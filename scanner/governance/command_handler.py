from datetime import datetime
from scanner.governance.approval_service import ApprovalService


class AdminCommandHandler:
    """
    Admin command routing layer.

    Rules:
    - Deterministic command dispatch
    - No direct scanner logic access
    - No implicit privilege escalation
    - All actions go through ApprovalService
    """

    def __init__(self, approval_service: ApprovalService):
        self.approval_service = approval_service

    def handle(self, command: str, admin_id: str, user_id: str) -> datetime:
        """
        Supported commands:
        - APPROVE_USER
        - BAN_USER
        """

        if command == "APPROVE_USER":
            return self.approval_service.approve_user(admin_id, user_id)

        if command == "BAN_USER":
            return self.approval_service.ban_user(admin_id, user_id)

        raise ValueError("UNKNOWN_COMMAND")
