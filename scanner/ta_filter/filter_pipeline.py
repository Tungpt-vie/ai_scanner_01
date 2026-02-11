from scanner.ta_engine.signal import TASignal
from scanner.ta_filter.fa_layer import FALayer, FAFilterDecision
from scanner.ta_filter.regime_layer import RegimeLayer
from scanner.ta_filter.pattern_layer import PatternLayer
from scanner.ta_filter.measurement_layer import MeasurementLayer
from scanner.ta_filter.level_layer import LevelLayer


class TAFilterPipeline:
    """
    Strict multi-layer filter pipeline.
    Order is LOCKED and must not change.

    1. FA Eligibility
    2. Regime Compatibility
    3. Pattern Strength
    4. Measurement Threshold
    5. Level Eligibility
    """

    def __init__(self):
        self.fa_layer = FALayer()
        self.regime_layer = RegimeLayer()
        self.pattern_layer = PatternLayer()
        self.measurement_layer = MeasurementLayer()
        self.level_layer = LevelLayer()

    def process(self, signal: TASignal, fa_status):
        """
        Return final decision:
        - DROP
        - OBSERVATION
        - STANDARD
        """

        # 1️⃣ FA Layer
        fa_decision = self.fa_layer.evaluate(fa_status)

        if fa_decision == FAFilterDecision.DROP:
            return "DROP"

        final_state = "STANDARD" if fa_decision == FAFilterDecision.STANDARD else "OBSERVATION"

        # 2️⃣ Regime Layer
        regime_result = self.regime_layer.evaluate(signal)

        if regime_result == "DROP":
            return "DROP"

        if regime_result == "DOWNGRADE":
            final_state = "OBSERVATION"

        # 3️⃣ Pattern Layer
        pattern_result = self.pattern_layer.evaluate(signal)

        if pattern_result == "DROP":
            return "DROP"

        if pattern_result == "DOWNGRADE":
            final_state = "OBSERVATION"

        # 4️⃣ Measurement Layer
        measurement_result = self.measurement_layer.evaluate(signal)

        if measurement_result == "DROP":
            return "DROP"

        if measurement_result == "DOWNGRADE":
            final_state = "OBSERVATION"

        # 5️⃣ Level Layer
        level_result = self.level_layer.evaluate(signal)

        if level_result == "DROP":
            return "DROP"

        if level_result == "DOWNGRADE":
            final_state = "OBSERVATION"

        return final_state
