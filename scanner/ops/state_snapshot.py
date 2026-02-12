from typing import Dict, Any
from datetime import datetime


class StateSnapshot:
    """
    Deterministic runtime state snapshot.

    Must NOT contain:
    - Rendered phrases
    - CTA text
    - Alert history
    - Event queue content

    Only structural runtime state.
    """

    def __init__(self):
        self._state: Dict[str, Any] = {}

    def capture(
        self,
        last_symbol: str,
        last_regime: str,
        last_filter_state: str,
        session_active: bool,
    ):
        """
        Capture minimal structural state required for safe resume.
        """

        self._state = {
            "timestamp": datetime.utcnow().isoformat(),
            "last_symbol": last_symbol,
            "last_regime": last_regime,
            "last_filter_state": last_filter_state,
            "session_active": session_active,
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Return current snapshot.
        """
        return dict(self._state)

    def clear(self):
        """
        Clear snapshot (e.g., hard reset).
        """
        self._state.clear()
