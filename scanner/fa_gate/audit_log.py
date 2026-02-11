from datetime import datetime
from scanner.fa_gate.store import FAStatus


class FAAuditLogger:
    """
    Log FA decisions for audit & observability.
    """

    @staticmethod
    def log_load_start():
        print(f"[{datetime.utcnow().isoformat()}] FA_LOAD_START")

    @staticmethod
    def log_load_done():
        print(f"[{datetime.utcnow().isoformat()}] FA_LOAD_DONE")

    @staticmethod
    def log_status(symbol: str, status: FAStatus):
        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"FA_STATUS | symbol={symbol} | status={status.value}"
        )

    @staticmethod
    def log_error(symbol: str):
        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"FA_DATA_ERROR | symbol={symbol}"
        )
