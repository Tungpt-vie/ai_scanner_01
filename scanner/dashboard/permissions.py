from fastapi import HTTPException
from scanner.security.auth_guard import AuthGuard


class DashboardPermission:
    """
    Read-only permission layer.

    Rules:
    - No privilege escalation
    - No role mutation
    - Read-only enforcement
    - Deterministic access checks
    """

    def __init__(self, auth_guard: AuthGuard):
        self.auth_guard = auth_guard

    def require_valid_token(self, token: str):
        if not token or not self.auth_guard.validate_token(token):
            raise HTTPException(status_code=403, detail="INVALID_TOKEN")

    def require_admin(self, admin_id: str):
        if not self.auth_guard.is_admin(admin_id):
            raise HTTPException(status_code=403, detail="ADMIN_NOT_FOUND")

    def require_user(self, user_id: str):
        if not self.auth_guard.is_user(user_id):
            raise HTTPException(status_code=403, detail="USER_NOT_FOUND")

    def can_view_admin_data(self, admin_id: str) -> bool:
        return self.auth_guard.is_admin(admin_id)

    def can_view_user_data(self, user_id: str) -> bool:
        return self.auth_guard.is_user(user_id)
