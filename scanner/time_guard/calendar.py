from datetime import date, datetime


class TradingCalendar:
    """
    Simple trading calendar for Vietnam stock market.
    Deterministic, no external dependency.
    """

    @staticmethod
    def is_trading_day(d: date | datetime) -> bool:
        """
        Return True if given date is a trading day.
        Monday (0) -> Friday (4) are trading days.
        """
        if isinstance(d, datetime):
            d = d.date()

        weekday = d.weekday()  # Monday=0 ... Sunday=6

        if weekday >= 5:
            return False

        return True
