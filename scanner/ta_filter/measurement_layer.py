from scanner.ta_engine.signal import TASignal


class MeasurementLayer:
    """
    Measurement Threshold Gate.

    Deterministic numeric validation.
    No promotion, only downgrade or drop.
    """

    def evaluate(self, signal: TASignal) -> str:
        """
        Return:
        - PASS
        - DOWNGRADE
        - DROP
        """

        measurements = signal.measurements

        rsi = measurements.get("rsi")
        volume_ratio = measurements.get("volume_ratio")

        # Missing key measurements → DROP
        if rsi is None or volume_ratio is None:
            return "DROP"

        # Extremely low volume participation → DROP
        if volume_ratio < 0.5:
            return "DROP"

        # Weak RSI zone → DOWNGRADE
        if 45 <= rsi <= 55:
            return "DOWNGRADE"

        return "PASS"
