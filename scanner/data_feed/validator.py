from datetime import datetime, time, timedelta


# VN stock market sessions (simplified, deterministic)
MORNING_START = time(9, 0)
MORNING_END = time(11, 30)
AFTERNOON_START = time(13, 0)
AFTERNOON_END = time(14, 45)


class CandleValidator:
    def __init__(self, timeframe_minutes: int):
        self.timeframe = timedelta(minutes=timeframe_minutes)

    def validate_structure(self, candle: dict):
        required_keys = {"timestamp", "open", "high", "low", "close", "volume"}
        if not candle:
            return False, "EMPTY_CANDLE"

        if not required_keys.issubset(candle.keys()):
            return False, "MISSING_KEYS"

        return True, "STRUCTURE_OK"

    def validate_ohlc(self, candle: dict):
        try:
            o = float(candle["open"])
            h = float(candle["high"])
            l = float(candle["low"])
            c = float(candle["close"])
        except Exception:
            return False, "NON_NUMERIC_OHLC"

        if l > h:
            return False, "LOW_GT_HIGH"

        if not (l <= o <= h and l <= c <= h):
            return False, "OHLC_OUT_OF_RANGE"

        return True, "OHLC_OK"

    def validate_volume(self, candle: dict):
        try:
            v = float(candle["volume"])
        except Exception:
            return False, "NON_NUMERIC_VOLUME"

        if v < 0:
            return False, "NEGATIVE_VOLUME"

        return True, "VOLUME_OK"

    def validate_session(self, ts: datetime):
        t = ts.time()
        in_morning = MORNING_START <= t <= MORNING_END
        in_afternoon = AFTERNOON_START <= t <= AFTERNOON_END

        if not (in_morning or in_afternoon):
            return False, "SESSION_MISMATCH"

        return True, "SESSION_OK"

    def detect_missing_bar(self, last_ts: datetime, current_ts: datetime):
        if last_ts is None:
            return False, "FIRST_CANDLE"

        expected_ts = last_ts + self.timeframe

        if current_ts != expected_ts:
            return True, "MISSING_BAR"

        return False, "NO_MISSING"

    def validate_candle(self, candle: dict, last_ts: datetime):
        # Structure
        ok, reason = self.validate_structure(candle)
        if not ok:
            return False, reason

        ts = candle["timestamp"]
        if not isinstance(ts, datetime):
            return False, "INVALID_TIMESTAMP"

        # Session
        ok, reason = self.validate_session(ts)
        if not ok:
            return False, reason

        # OHLC
        ok, reason = self.validate_ohlc(candle)
        if not ok:
            return False, reason

        # Volume
        ok, reason = self.validate_volume(candle)
        if not ok:
            return False, reason

        # Missing bar
        missing, reason = self.detect_missing_bar(last_ts, ts)
        if missing:
            return False, reason

        return True, "CANDLE_OK"
