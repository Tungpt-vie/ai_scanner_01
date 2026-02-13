from typing import List
from scanner.governance.watchlist_repository import WatchlistRepository


class WatchlistRouter:
    """
    User-target resolution layer.

    Responsibilities:
    - Determine which users are interested in a symbol
    - No scanner coupling
    - No cross-channel mixing
    - Deterministic
    """

    def __init__(self, watchlist_repo: WatchlistRepository):
        self.watchlist_repo = watchlist_repo

    def resolve_users_for_symbol(self, symbol: str) -> List[str]:
        """
        Return list of user_ids whose watchlist contains the symbol.
        """

        normalized = symbol.strip().upper()
        matched_users = []

        for watchlist in self.watchlist_repo.list_all():
            if watchlist.has_symbol(normalized):
                matched_users.append(watchlist.user_id)

        return matched_users
