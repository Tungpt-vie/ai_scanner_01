from datetime import datetime
from scanner.ta_engine.signal import TASignal
from scanner.event_generator.schema import TAEvent


class TAEventFactory:
    """
    Deterministic factory for TAEvent.
    No transformation beyond normalization.
    """

    def create_event(
        self,
        symbol: str,
        timestamp: datetime,
        signal: TASignal,
        filter_state: str,
    ) -> TAEvent:
        """
        Create immutable TAEvent from evaluated signal.
        """

        return TAEvent(
            symbol=symbol,
            timestamp=timestamp,
            regime=signal.regime.value,
            ta_state=signal.ta_state,
            filter_state=filter_state,
            confidence=signal.confidence,
            patterns=signal.patterns,
            measurements=signal.measurements,
        )
