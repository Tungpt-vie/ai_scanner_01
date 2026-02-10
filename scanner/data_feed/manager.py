from typing import List
from scanner.data_feed.validator import CandleValidator


class FeedManager:
    def __init__(self, feeds: List, timeframe_minutes: int):
        self.feeds = feeds
        self.active_index = 0
        self.active_feed = self.feeds[self.active_index]

        self.validator = CandleValidator(timeframe_minutes)
        self.last_valid_timestamp = None

        self.suppress_alerts = True

    def switch_source(self, reason: str):
        old_source = self.active_feed.__class__.__name__

        self.active_index += 1
        if self.active_index >= len(self.feeds):
            raise RuntimeError("NO_DATA_SOURCE_AVAILABLE")

        self.active_feed = self.feeds[self.active_index]
        self.active_feed.reset_state()

        self.last_valid_timestamp = None
        self.suppress_alerts = True

        print(
            f"SOURCE_SWITCH | from={old_source} "
            f"to={self.active_feed.__class__.__name__} | reason={reason}"
        )

    def get_latest_valid_candle(self):
        try:
            candle = self.active_feed.fetch_latest_candle()
        except Exception as e:
            self.switch_source(f"EXCEPTION: {e}")
            return None

        if candle is None:
            self.switch_source("EMPTY_CANDLE")
            return None

        ok, reason = self.validator.validate_candle(
            candle, self.last_valid_timestamp
        )

        if not ok:
            self.active_feed.mark_invalid(reason)
            self.suppress_alerts = True
            return None

        # Candle is valid
        self.last_valid_timestamp = candle["timestamp"]
        self.active_feed.mark_valid()

        # After first valid candle, alerts may resume
        self.suppress_alerts = False
        return candle
