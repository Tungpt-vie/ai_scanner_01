from datetime import datetime, time
from enum import Enum


class TradingSession(Enum):
    MORNING = "MORNING"
    BREAK = "BREAK"
    AFTERNOON = "AFTERNOON"
    ATC = "ATC"
    OUT = "OUT_OF_SESSION"


MORNING_START = time(9, 0)
MORNING_END = time(11, 30)

AFTERNOON_START = time(13, 0)
AFTERNOON_END = time(14, 45)

ATC_START = time(14, 45)
ATC_END = time(15, 0)


def detect_session(ts: datetime) -> TradingSession:
    """
    Detect trading session from timestamp.
    """
    t = ts.time()

    if MORNING_START <= t < MORNING_END:
        return TradingSession.MORNING

    if MORNING_END <= t < AFTERNOON_START:
        return TradingSession.BREAK

    if AFTERNOON_START <= t < AFTERNOON_END:
        return TradingSession.AFTERNOON

    if ATC_START <= t < ATC_END:
        return TradingSession.ATC

    return TradingSession.OUT
