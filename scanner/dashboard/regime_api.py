from scanner.optimization.regime_cache import RegimeCache
from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.dashboard.regime_service import MarketRegimeService
from scanner.dashboard.regime_serializer import MarketRegimeSerializer
from scanner.optimization.regime_cache import RegimeCache
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (cache binding only)
# ----------------------------

regime_cache = RegimeCache()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

regime_service = MarketRegimeService(regime_cache)
serializer = MarketRegimeSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(prefix="/regime", tags=["Market Regime"])


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_market_regime(
    authorization: str = Security(api_key_header),
):
    """
    Return current market regime snapshot.

    - Cache-only
    - No recompute
    - No scan trigger
    - Read-only
    """

    permissions.require_valid_token(authorization)

    regime_data = regime_service.get_current_regime()
    metadata = regime_service.get_regime_metadata()

    return serializer.serialize(regime_data, metadata)
