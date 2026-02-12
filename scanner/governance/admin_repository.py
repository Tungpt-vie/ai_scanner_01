from typing import Dict
from scanner.governance.admin_model import Admin


class AdminRepository:
    """
    Deterministic in-memory admin repository.

    Rules:
    - No auto-create
    - No implicit role change
    - Explicit add only
    """

    def __init__(self):
        self._admins: Dict[str, Admin] = {}

    def add(self, admin: Admin):
        if admin.admin_id in self._admins:
            raise ValueError("ADMIN_ALREADY_EXISTS")
        self._admins[admin.admin_id] = admin

    def get(self, admin_id: str) -> Admin:
        if admin_id not in self._admins:
            raise ValueError("ADMIN_NOT_FOUND")
        return self._admins[admin_id]

    def exists(self, admin_id: str) -> bool:
        return admin_id in self._admins

    def list_all(self):
        return list(self._admins.values())
