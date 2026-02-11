from scanner.fa_gate.store import FAStatus


class EarlyDropEngine:
    """
    Early-drop optimization layer.

    Purpose:
    - Avoid unnecessary downstream computation
    - Never alter logic outcome
    - Only drop cases that are deterministically invalid
    """

    def check_data_sufficiency(self, context, min_bars: int = 20) -> bool:
        """
        Ensure enough bars for regime detection.
        """
        return context.size() >= min_bars

    def check_fa_hard_drop(self, fa_status: FAStatus) -> bool:
        """
        If FA_FAIL → hard drop immediately.
        """
        return fa_status != FAStatus.FA_FAIL

    def check_session_boundary(self, is_session_active: bool) -> bool:
        """
        If outside session → drop early.
        """
        return is_session_active

    def check_silence_rule(self, last_filter_state: str, current_filter_state: str) -> bool:
        """
        Prevent reprocessing identical DROP states.
        """
        if last_filter_state == "DROP" and current_filter_state == "DROP":
            return False
        return True

    def allow_processing(
        self,
        context,
        fa_status: FAStatus,
        is_session_active: bool,
    ) -> bool:
        """
        Combined early-drop decision.
        """

        if not self.check_session_boundary(is_session_active):
            return False

        if not self.check_data_sufficiency(context):
            return False

        if not self.check_fa_hard_drop(fa_status):
            return False

        return True
