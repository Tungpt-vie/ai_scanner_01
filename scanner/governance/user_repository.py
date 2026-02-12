from typing import Dict
from scanner.governance.user_model import User


class UserRepository:
    """
    Deterministic in-memory user repository.

    Rules:
    - No auto-create
    - No implicit upgrade
    - Explicit lifecycle only
    """

    def __init__(self):
        self._users: Dict[str, User] = {}

    def add(self, user: User):
        if user.user_id in self._users:
            raise ValueError("USER_ALREADY_EXISTS")
        self._users[user.user_id] = user

    def get(self, user_id: str) -> User:
        if user_id not in self._users:
            raise ValueError("USER_NOT_FOUND")
        return self._users[user_id]

    def exists(self, user_id: str) -> bool:
        return user_id in self._users

    def list_all(self):
        return list(self._users.values())

    def remove(self, user_id: str):
        if user_id not in self._users:
            raise ValueError("USER_NOT_FOUND")
        del self._users[user_id]
