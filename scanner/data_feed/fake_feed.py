from datetime import datetime, timedelta
from scanner.data_feed.base_feed import BaseFeed


class FakeFeed(BaseFeed):
    """
    Fake feed for testing failover & validation logic.
    """

    def __init__(self, symbol: str, timeframe_minutes: int):
        super().__init__(symbol, str(timeframe_minutes) + "m")
        self.current_time = None
        self.step = 0
        self.tf = timedelta(minutes=timeframe_minutes)

    def fetch_latest_candle(self):
        # First call: valid candle
        if self.step == 0:
            self.current_time = datetime(2024, 1, 2, 9, 0)
        # Second call: valid next candle
        elif self.step == 1:
            self.current_time = self.current_time + self.tf
        # Third call: MISSING BAR (skip one)
        elif self.step == 2:
            self.current_time = self.current_time + self.tf * 2
        # Fourth call: session mismatch
        elif self.step == 3:
            self.current_time = datetime(2024, 1, 2, 12, 0)
        else:
            return None

        self.step += 1

        return {
            "timestamp": self.current_time,
            "open": 10.0,
            "high": 11.0,
            "low": 9.5,
            "close": 10.5,
            "volume": 1000.0,
        }
