from datetime import datetime, date
from scanner.time_guard.session import TradingSession, detect_session


class SessionState:
    """
    Keep track of trading day and session transitions.
    """

    def __init__(self):
        self.current_day: date | None = None
        self.current_session: TradingSession | None = None

    def update(self, ts: datetime):
        ts_date = ts.date()
        session = detect_session(ts)

        day_changed = False
        session_changed = False

        # New trading day
        if self.current_day != ts_date:
            self.current_day = ts_date
            self.current_session = session
            day_changed = True
            session_changed = True
            return day_changed, session_changed, session

        # Same day, session change
        if session != self.current_session:
            self.current_session = session
            session_changed = True

        return day_changed, session_changed, session

    def reset(self):
        self.current_day = None
        self.current_session = None
