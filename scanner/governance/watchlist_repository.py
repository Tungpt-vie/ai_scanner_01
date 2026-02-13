from typing import Dict
from scanner.governance.watchlist_model import UserWatchlist


class WatchlistRepository:
    """
    Deterministic in-memory watchlist repository.

    Rules:
    - No auto-create on get
    - Explicit add only
    - One watchlist per user
    - No scanner coupling
    """

    def __init__(self):
        self._watchlists: Dict[str, UserWatchlist] = {}

    def add(self, watchlist: UserWatchlist):
        if watchlist.user_id in self._watchlists:
            raise ValueError("WATCHLIST_ALREADY_EXISTS")
        self._watchlists[watchlist.user_id] = watchlist

    def get(self, user_id: str) -> UserWatchlist:
        if user_id not in self._watchlists:
            raise ValueError("WATCHLIST_NOT_FOUND")
        return self._watchlists[user_id]

    def exists(self, user_id: str) -> bool:
        return user_id in self._watchlists

    def remove(self, user_id: str):
        if user_id not in self._watchlists:
            raise ValueError("WATCHLIST_NOT_FOUND")
        del self._watchlists[user_id]

    def list_all(self):
        return list(self._watchlists.values())
