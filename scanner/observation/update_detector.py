from typing import Dict


class ObservationUpdateDetector:
    """
    Detect whether an observation has meaningful change.

    Rules:
    - No escalation to STANDARD
    - No TA mutation
    - Pure deterministic comparison
    - Stateless
    """

    def has_meaningful_change(
        self,
        previous_measurements: Dict[str, float],
        current_measurements: Dict[str, float],
        threshold: float = 0.01,
    ) -> bool:
        """
        Compare measurement deltas.

        threshold default: 1% relative change
        """

        for key, current_value in current_measurements.items():

            if key not in previous_measurements:
                return True

            previous_value = previous_measurements[key]

            if previous_value is None or current_value is None:
                continue

            if previous_value == 0:
                if current_value != 0:
                    return True
                continue

            relative_change = abs(current_value - previous_value) / abs(previous_value)

            if relative_change >= threshold:
                return True

        return False
