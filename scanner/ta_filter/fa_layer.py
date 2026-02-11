from enum import Enum
from scanner.fa_gate.store import FAStatus


class FAFilterDecision(Enum):
    DROP = "DROP"
    OBSERVATION = "OBSERVATION"
    STANDARD = "STANDARD"


class FALayer:
    """
    FA Eligibility Layer.

    Rules:
    - FA_FAIL     → DROP
    - FA_UNKNOWN  → OBSERVATION
    - FA_PASS     → STANDARD
    """

    def evaluate(self, fa_status: FAStatus) -> FAFilterDecision:

        if fa_status == FAStatus.FA_FAIL:
            return FAFilterDecision.DROP

        if fa_status == FAStatus.FA_UNKNOWN:
            return FAFilterDecision.OBSERVATION

        if fa_status == FAStatus.FA_PASS:
            return FAFilterDecision.STANDARD

        # Safety fallback (should never happen)
        return FAFilterDecision.DROP
