from scanner.event_generator.schema import TAEvent


class ChannelGuard:
    """
    Channel isolation layer.

    This layer ensures:
    - DROP events never propagate
    - OBSERVATION and STANDARD are allowed internally
    - No external side-effect is triggered
    """

    def allow(self, event: TAEvent) -> bool:
        """
        Determine whether event is allowed to pass to internal emitter.
        """

        if event.filter_state == "DROP":
            return False

        # OBSERVATION and STANDARD are allowed
        return True
