from enum import Enum
from typing import Dict


class FAStatus(Enum):
    FA_PASS = "FA_PASS"
    FA_FAIL = "FA_FAIL"
    FA_UNKNOWN = "FA_UNKNOWN"


class FASnapshotStore:
    """
    Store FA snapshot (offline batch).
    Freeze during trading session.
    """

    def __init__(self):
        self._snapshot: Dict[str, FAStatus] = {}
        self._frozen = False

    def load_snapshot(self, data: Dict[str, FAStatus]):
        """
        Load FA snapshot (offline only).
        """
        if self._frozen:
            raise RuntimeError("FA_SNAPSHOT_FROZEN")

        self._snapshot = data.copy()
        print("[FA_GATE] FA_LOAD_DONE")

    def freeze(self):
        """
        Freeze FA snapshot during trading session.
        """
        self._frozen = True

    def unfreeze(self):
        """
        Allow reload (outside trading session).
        """
        self._frozen = False

    def get_status(self, symbol: str) -> FAStatus:
        """
        Return FA status for symbol.
        """
        return self._snapshot.get(symbol, FAStatus.FA_UNKNOWN)

    def is_frozen(self) -> bool:
        return self._frozen
