from typing import List, Dict

from scanner.storage.event_repository import EventRepository
from scanner.analytics.export_validator import ExportValidator
from scanner.analytics.csv_generator import CSVGenerator


class ExportService:
    """
    PRO-only export service.
    Read-only.
    Deterministic.
    """

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def export_events(self, user_role: str) -> str:
        ExportValidator.validate_pro_access(user_role)

        events = self.event_repository.list_all()

        dataset: List[Dict] = []

        for event in events:
            dataset.append({
                "symbol": getattr(event, "symbol", None),
                "event_type": getattr(event, "event_type", None),
                "regime_state": getattr(event, "regime_state", None),
                "timestamp": getattr(event, "timestamp", None),
            })

        ExportValidator.validate_row_limit(dataset)

        return CSVGenerator.generate(dataset)
