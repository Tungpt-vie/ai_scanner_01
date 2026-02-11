from typing import Dict


class SimpleCacheStore:
    """
    Simple in-memory cache store.

    - No disk persistence
    - No TTL
    - No auto-expiry
    - Reset manually only
    """

    def __init__(self):
        self._store: Dict[str, str] = {}

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value: str):
        self._store[key] = value

    def exists(self, key: str) -> bool:
        return key in self._store

    def clear(self):
        self._store.clear()
