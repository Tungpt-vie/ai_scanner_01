from abc import ABC, abstractmethod
from datetime import datetime


class BaseFeed(ABC):
    """
    Base interface for ALL market data feeds.
    All concrete feeds MUST follow these rules strictly.
    """

    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe

        # Internal state
        self.last_candle_time = None
        self.data_valid = True

    @abstractmethod
    def fetch_latest_candle(self):
        """
        Fetch latest OHLCV candle.

        MUST return dict with keys:
        {
            "timestamp": datetime,
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float
        }

        OR return None if data unavailable.
        """
        pass

    def reset_state(self):
        """
        Reset internal state.
        Called on source switch or hard failure.
        """
        self.last_candle_time = None
        self.data_valid = True

    def mark_invalid(self, reason: str):
        """
        Mark data as invalid.
        System must go silent when this happens.
        """
        self.data_valid = False
        self.log_event("DATA_INVALID", reason)

    def mark_valid(self):
        """
        Mark data as valid again.
        """
        self.data_valid = True
        self.log_event("DATA_OK", "data restored")

    def log_event(self, event: str, reason: str):
        """
        Basic log hook.
        Concrete implementation can override.
        """
        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"{event} | source={self.__class__.__name__} | "
            f"symbol={self.symbol} | tf={self.timeframe} | reason={reason}"
        )
