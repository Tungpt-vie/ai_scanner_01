from typing import Dict
from scanner.ta_engine.regime import MarketRegime


class PatternDetector:
    """
    Locked deterministic pattern set.
    No expansion beyond predefined logic.
    """

    def detect(self, regime: MarketRegime, measurements: Dict) -> Dict[str, bool]:
        """
        Return pattern states.
        """

        patterns = {
            "momentum_expansion": False,
            "mean_reversion_setup": False,
            "volatility_breakout": False,
            "compression_break": False,
        }

        rsi = measurements.get("rsi")
        volume_ratio = measurements.get("volume_ratio")
        structure_age = measurements.get("structure_age")

        if rsi is None:
            return patterns

        # TRENDING regime logic
        if regime == MarketRegime.TRENDING:
            if rsi > 60 and volume_ratio and volume_ratio > 1.2:
                patterns["momentum_expansion"] = True

        # RANGING regime logic
        if regime == MarketRegime.RANGING:
            if rsi < 35 or rsi > 65:
                patterns["mean_reversion_setup"] = True

        # VOLATILE regime logic
        if regime == MarketRegime.VOLATILE:
            if volume_ratio and volume_ratio > 1.5:
                patterns["volatility_breakout"] = True

        # COMPRESSION regime logic
        if regime == MarketRegime.COMPRESSION:
            if structure_age is not None and structure_age < 3:
                patterns["compression_break"] = True

        return patterns
