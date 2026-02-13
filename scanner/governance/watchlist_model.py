from dataclasses import dataclass, field
from typing import Set


@dataclass
class UserWatchlist:
    """
    Per-user watchlist model.

    Rules:
    - Independent from scanner logic
    - No auto-add from system
    - Explicit symbol management only
    - Case-normalized symbols
    """

    user_id: str
    symbols: Set[str] = field(default_factory=set)

    def add_symbol(self, symbol: str):
        normalized = symbol.strip().upper()

        if not normalized:
            raise ValueError("INVALID_SYMBOL")

        self.symbols.add(normalized)

    def remove_symbol(self, symbol: str):
        normalized = symbol.strip().upper()

        if normalized not in self.symbols:
            raise ValueError("SYMBOL_NOT_IN_WATCHLIST")

        self.symbols.remove(normalized)

    def has_symbol(self, symbol: str) -> bool:
        return symbol.strip().upper() in self.symbols

    def list_symbols(self):
        return sorted(self.symbols)
