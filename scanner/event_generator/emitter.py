from typing import List
from scanner.event_generator.schema import TAEvent
from scanner.event_generator.channel_guard import ChannelGuard
from scanner.event_generator.deduplicator import EventDeduplicator


class InternalEventEmitter:
    """
    Internal event emitter.

    - No external API call
    - No notification
    - No persistence
    - Only in-memory queue
    """

    def __init__(self):
        self.guard = ChannelGuard()
        self.deduplicator = EventDeduplicator()
        self._queue: List[TAEvent] = []

    def emit(self, event: TAEvent) -> bool:
        """
        Attempt to emit event.

        Return True if emitted.
        """

        # 1️⃣ Channel guard
        if not self.guard.allow(event):
            return False

        # 2️⃣ Deduplication
        if self.deduplicator.is_duplicate(event):
            return False

        # 3️⃣ Internal enqueue
        self._queue.append(event)
        return True

    def get_events(self) -> List[TAEvent]:
        """
        Return current internal queue.
        """
        return list(self._queue)

    def reset(self):
        """
        Reset emitter state (e.g., new session).
        """
        self._queue.clear()
        self.deduplicator.reset()
