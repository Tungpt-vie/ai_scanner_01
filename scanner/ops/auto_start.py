from scanner.ops.resume_manager import ResumeManager
from scanner.ops.internet_watchdog import InternetWatchdog


class AutoStartController:
    """
    Safe auto-start controller.

    Responsibilities:
    - Wait for internet if needed
    - Attempt safe resume
    - Never replay events
    - Never backfill historical data
    """

    def __init__(self):
        self.resume_manager = ResumeManager()
        self.watchdog = InternetWatchdog()
        self._started = False

    def start(self) -> bool:
        """
        Safe system start.

        Steps:
        1. Ensure internet connectivity
        2. Attempt silent resume
        3. Do not replay
        """

        # 1️⃣ Ensure connectivity (silent wait if offline)
        if not self.watchdog.check_connection():
            self.watchdog.wait_until_online()

        # 2️⃣ Attempt resume (silent)
        resume_allowed = self.resume_manager.attempt_resume()

        self._started = resume_allowed
        return resume_allowed

    def is_started(self) -> bool:
        return self._started

    def reset(self):
        """
        Hard reset controller.
        """
        self.resume_manager.reset()
        self._started = False
