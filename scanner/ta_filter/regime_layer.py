from scanner.ta_engine.regime import MarketRegime
from scanner.ta_engine.signal import TASignal


class RegimeLayer:
    """
    Regime Compatibility Gate.

    - Do not upgrade signal.
    - Only downgrade or drop.
    """

    def evaluate(self, signal: TASignal) -> str:
        """
        Return:
        - PASS
        - DOWNGRADE
        - DROP
        """

        regime = signal.regime
        ta_state = signal.ta_state

        # UNKNOWN regime → DROP
        if regime == MarketRegime.UNKNOWN:
            return "DROP"

        # If regime is COMPRESSION and signal is VALID → downgrade
        if regime == MarketRegime.COMPRESSION and ta_state == "VALID":
            return "DOWNGRADE"

        # If regime is VOLATILE and confidence is weak → downgrade
        if regime == MarketRegime.VOLATILE and signal.confidence < 0.5:
            return "DOWNGRADE"

        return "PASS"
