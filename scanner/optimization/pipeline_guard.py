from scanner.optimization.early_drop import EarlyDropEngine
from scanner.optimization.regime_cache import RegimeCache
from scanner.fa_gate.store import FAStatus


class OptimizationGuard:
    """
    Optimization guard layer.

    Integrates:
    - Early-drop checks
    - Regime caching

    This layer MUST NOT:
    - Modify TA logic
    - Override filter logic
    - Promote signal state
    """

    def __init__(self):
        self.early_drop = EarlyDropEngine()
        self.regime_cache = RegimeCache()

    def should_process(
        self,
        symbol: str,
        context,
        fa_status: FAStatus,
        is_session_active: bool,
    ) -> bool:
        """
        Decide whether full pipeline processing should proceed.
        """

        return self.early_drop.allow_processing(
            context=context,
            fa_status=fa_status,
            is_session_active=is_session_active,
        )

    def get_regime(self, symbol: str, context):
        """
        Return regime using cache wrapper.
        """

        return self.regime_cache.get_regime(symbol, context.closes)

    def reset(self):
        """
        Reset optimization state (e.g., new trading day).
        """
        self.regime_cache.reset()
