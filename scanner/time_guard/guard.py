from datetime import datetime
from scanner.time_guard.calendar import TradingCalendar
from scanner.time_guard.session import TradingSession
from scanner.time_guard.state import SessionState


class TimeGuard:
    """
    Time & Session guard.
    Decide whether a candle/event is allowed to pass.
    """

    def __init__(self):
        self.calendar = TradingCalendar()
        self.state = SessionState()
        self.suppress_alerts = True

    def allow(self, ts: datetime) -> bool:
        """
        Return True if processing is allowed at this timestamp.
        """
        # Trading day check
        if not self.calendar.is_trading_day(ts):
            self.suppress_alerts = True
            self._log("NO_TRADING_DAY", ts)
            return False

        day_changed, session_changed, session = self.state.update(ts)

        # Day boundary rule
        if day_changed:
            self.suppress_alerts = True
            self._log("DAY_RESET", ts)

        # Session change handling
        if session_changed:
            if session == TradingSession.BREAK:
                self.suppress_alerts = True
                self._log("SESSION_BREAK", ts)
                return False

            if session in (
                TradingSession.MORNING,
                TradingSession.AFTERNOON,
                TradingSession.ATC,
            ):
                # Resume after break: suppress until first full candle
                self.suppress_alerts = True
                self._log("SESSION_START", ts)

        # Block non-trading sessions
        if session in (TradingSession.BREAK, TradingSession.OUT):
            self._log("OUT_OF_SESSION_DROP", ts)
            return False

        # Allow processing, but alerts may still be suppressed
        self.suppress_alerts = False
        return True

    def _log(self, event: str, ts: datetime):
        print(
            f"[TIME_GUARD] {event} | "
            f"time={ts.isoformat()} | "
            f"suppress_alerts={self.suppress_alerts}"
        )
