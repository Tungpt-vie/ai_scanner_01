from typing import List, Dict
from datetime import datetime


class DurationAnalysis:
    """
    CLOSED observation duration computation.
    Deterministic.
    No mutation.
    """

    @staticmethod
    def compute_durations(observations: List[Dict]) -> List[int]:
        durations = []

        for obs in observations:
            created_at = obs.get("created_at")
            closed_at = obs.get("updated_at")

            if not created_at or not closed_at:
                continue

            try:
                start = datetime.fromisoformat(created_at)
                end = datetime.fromisoformat(closed_at)
                duration_seconds = int((end - start).total_seconds())
                if duration_seconds >= 0:
                    durations.append(duration_seconds)
            except Exception:
                continue

        return durations
