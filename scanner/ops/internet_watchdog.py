import socket
import time


class InternetWatchdog:
    """
    Simple internet connectivity watchdog.

    Rules:
    - No auto-trade
    - No alert
    - No retry storm
    - Silent detection only
    """

    def __init__(self, host: str = "8.8.8.8", port: int = 53, timeout: int = 3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._online = True

    def check_connection(self) -> bool:
        """
        Attempt TCP connection to detect connectivity.
        """

        try:
            socket.setdefaulttimeout(self.timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (self.host, self.port)
            )
            self._online = True
        except Exception:
            self._online = False

        return self._online

    def is_online(self) -> bool:
        return self._online

    def wait_until_online(self, interval: int = 5):
        """
        Block until internet returns.
        Silent wait.
        """

        while not self.check_connection():
            time.sleep(interval)
