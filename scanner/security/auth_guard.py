from typing import Dict
from scanner.governance.admin_repository import AdminRepository
from scanner.governance.user_repository import UserRepository


class AuthGuard:
    """
    Authentication & role verification guard.

    Rules:
    - No implicit privilege escalation
    - No scanner access
    - Deterministic validation
    - Token validation stub only (no external auth integration)
    """

    def __init__(
        self,
        admin_repo: AdminRepository,
        user_repo: UserRepository,
    ):
        self.admin_repo = admin_repo
        self.user_repo = user_repo

    def validate_token(self, token: str) -> bool:
        """
        Stub token validation.
        In production, replace with real verification.
        """
        if not token or not isinstance(token, str):
            return False

        # Deterministic stub rule:
        # Token must start with "TOKEN_"
        return token.startswith("TOKEN_")

    def is_admin(self, admin_id: str) -> bool:
        return self.admin_repo.exists(admin_id)

    def is_user(self, user_id: str) -> bool:
        return self.user_repo.exists(user_id)

    def require_admin(self, admin_id: str):
        if not self.is_admin(admin_id):
            raise PermissionError("ADMIN_NOT_FOUND")

    def require_user(self, user_id: str):
        if not self.is_user(user_id):
            raise PermissionError("USER_NOT_FOUND")
