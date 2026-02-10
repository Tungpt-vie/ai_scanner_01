from datetime import datetime
from scanner.time_guard.guard import TimeGuard

guard = TimeGuard()

tests = [
    # Before market
    datetime(2024, 1, 2, 8, 30),

    # Morning session
    datetime(2024, 1, 2, 9, 5),
    datetime(2024, 1, 2, 10, 0),

    # Lunch break
    datetime(2024, 1, 2, 11, 45),

    # Afternoon resume
    datetime(2024, 1, 2, 13, 5),

    # ATC
    datetime(2024, 1, 2, 14, 50),

    # After hours
    datetime(2024, 1, 2, 15, 10),

    # Next day
    datetime(2024, 1, 3, 9, 5),
]

for ts in tests:
    allowed = guard.allow(ts)
    print(f"{ts} -> ALLOW={allowed}")
