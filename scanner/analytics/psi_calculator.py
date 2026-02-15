from typing import Dict
from math import log


class PSICalculator:
    """
    Pattern Stability Index (PSI)

    Deterministic.
    No prediction.
    No ranking.
    No CTA.
    """

    @staticmethod
    def compute(pattern_frequency: Dict[str, int]) -> Dict[str, float]:
        total = sum(pattern_frequency.values())

        if total == 0:
            return {}

        psi_scores: Dict[str, float] = {}

        for pattern, count in pattern_frequency.items():
            p = count / total

            if p <= 0:
                continue

            # Stability = -p * log(p)
            psi_scores[pattern] = round(-p * log(p), 6)

        return psi_scores
