from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass(frozen=True)
class TAEvent:
    """
    Immutable TA Event object.

    No BUY / SELL.
    No action directive.
    No external routing.
    Pure state container.
    """

    symbol: str
    timestamp: datetime
    regime: str
    ta_state: str              # NO_SIGNAL / WEAK / VALID
    filter_state: str          # DROP / OBSERVATION / STANDARD
    confidence: float
    patterns: Dict[str, bool]
    measurements: Dict[str, float | None]

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "regime": self.regime,
            "ta_state": self.ta_state,
            "filter_state": self.filter_state,
            "confidence": self.confidence,
            "patterns": self.patterns,
            "measurements": self.measurements,
        }
