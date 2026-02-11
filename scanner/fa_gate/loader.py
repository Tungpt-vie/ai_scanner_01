from typing import Dict
from scanner.fa_gate.evaluator import FAEvaluator
from scanner.fa_gate.store import FASnapshotStore, FAStatus


class FALoader:
    """
    Offline FA batch loader.
    Must be called EOD or pre-market only.
    """

    def __init__(self, store: FASnapshotStore, min_avg_value_traded: float):
        self.store = store
        self.evaluator = FAEvaluator(min_avg_value_traded)

    def load_batch(self, raw_fa_data: Dict[str, Dict]):
        """
        raw_fa_data format:
        {
            "VCB": {...},
            "HPG": {...}
        }
        """

        print("[FA_GATE] FA_LOAD_START")

        snapshot: Dict[str, FAStatus] = {}

        for symbol, data in raw_fa_data.items():
            status = self.evaluator.evaluate(symbol, data)
            snapshot[symbol] = status

        self.store.load_snapshot(snapshot)
