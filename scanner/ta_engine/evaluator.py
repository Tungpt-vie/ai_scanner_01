from scanner.ta_engine.regime import RegimeDetector, MarketRegime
from scanner.ta_engine.measurements import MeasurementExtractor
from scanner.ta_engine.patterns import PatternDetector
from scanner.ta_engine.signal import TASignal


class TAEvaluator:
    """
    Regime-first deterministic TA evaluation core.
    No prediction. No BUY/SELL.
    """

    def __init__(self):
        self.regime_detector = RegimeDetector()
        self.measurements = MeasurementExtractor()
        self.patterns = PatternDetector()

    def evaluate(self, context) -> TASignal:

        # 1️⃣ Regime-first rule
        regime = self.regime_detector.detect(context.closes)

        # 2️⃣ Extract measurements
        measurement_data = self.measurements.extract(context)

        # 3️⃣ Detect patterns (regime-aware)
        pattern_states = self.patterns.detect(regime, measurement_data)

        # 4️⃣ Compute deterministic confidence
        active_patterns = sum(1 for v in pattern_states.values() if v)

        confidence = min(active_patterns / 4, 1.0)

        # 5️⃣ Determine TA state
        if active_patterns == 0:
            ta_state = "NO_SIGNAL"
        elif confidence < 0.5:
            ta_state = "WEAK"
        else:
            ta_state = "VALID"

        return TASignal(
            regime=regime,
            patterns=pattern_states,
            measurements=measurement_data,
            confidence=confidence,
            ta_state=ta_state,
        )
