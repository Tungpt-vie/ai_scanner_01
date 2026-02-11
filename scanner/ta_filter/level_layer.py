from scanner.ta_engine.signal import TASignal


class LevelLayer:
    """
    Final structural eligibility gate.

    This layer ensures signal quality based on structural stability.
    No promotion allowed.
    """

    def evaluate(self, signal: TASignal) -> str:
        """
        Return:
        - PASS
        - DOWNGRADE
        - DROP
        """

        measurements = signal.measurements

        structure_age = measurements.get("structure_age")

        # Missing structural info → DROP
        if structure_age is None:
            return "DROP"

        # Structure too fresh (break not confirmed) → DOWNGRADE
        if structure_age < 2:
            return "DOWNGRADE"

        return "PASS"
