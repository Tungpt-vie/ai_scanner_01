from typing import List, Dict


class TAContext:
    """
    Hold rolling OHLCV data for TA engine.
    Deterministic, no auto-trim unless specified.
    """

    def __init__(self, max_length: int = 500):
        self.max_length = max_length

        self.opens: List[float] = []
        self.highs: List[float] = []
        self.lows: List[float] = []
        self.closes: List[float] = []
        self.volumes: List[float] = []

    def add_candle(self, candle: Dict):
        """
        Add validated candle.
        """

        self.opens.append(candle["open"])
        self.highs.append(candle["high"])
        self.lows.append(candle["low"])
        self.closes.append(candle["close"])
        self.volumes.append(candle["volume"])

        self._trim_if_needed()

    def _trim_if_needed(self):
        """
        Keep rolling window bounded.
        """

        if len(self.closes) > self.max_length:
            self.opens.pop(0)
            self.highs.pop(0)
            self.lows.pop(0)
            self.closes.pop(0)
            self.volumes.pop(0)

    def size(self) -> int:
        return len(self.closes)
