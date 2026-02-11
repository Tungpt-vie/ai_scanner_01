from dataclasses import dataclass
from typing import Dict
from scanner.ta_engine.regime import MarketRegime


@dataclass
class TASignal:
    """
    Normalized TA Signal object.
    No BUY / SELL.
    Deterministic state container only.
    """

    regime: MarketRegime
    patterns: Dict[str, bool]
    measurements: Dict[str, float | None]
    confidence: float
    ta_state: str  # NO_SIGNAL / WEAK / VALID

    def to_dict(self) -> Dict:
        return {
            "regime": self.regime.value,
            "patterns": self.patterns,
            "measurements": self.measurements,
            "confidence": self.confidence,
            "ta_state": self.ta_state,
        }
