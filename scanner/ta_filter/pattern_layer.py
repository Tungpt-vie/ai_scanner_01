from scanner.ta_engine.signal import TASignal


class PatternLayer:
    """
    Pattern Strength Gate.

    - If no active pattern → DROP
    - If only 1 active pattern → DOWNGRADE
    - If >=2 active patterns → PASS
    """

    def evaluate(self, signal: TASignal) -> str:
        """
        Return:
        - PASS
        - DOWNGRADE
        - DROP
        """

        active_patterns = sum(1 for v in signal.patterns.values() if v)

        if active_patterns == 0:
            return "DROP"

        if active_patterns == 1:
            return "DOWNGRADE"

        return "PASS"
