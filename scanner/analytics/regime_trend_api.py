from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.analytics.regime_trend_service import RegimeTrendService
from scanner.analytics.regime_trend_serializer import RegimeTrendSerializer
from scanner.storage.event_repository import EventRepository
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (read-only binding)
# ----------------------------

event_repository = EventRepository()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

service = RegimeTrendService(event_repository)
serializer = RegimeTrendSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="/analytics/regime-trend",
    tags=["Analytics"]
)


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_regime_trend(
    authorization: str = Security(api_key_header),
):
    """
    Read-only Regime Trend Analytics.

    - No prediction
    - No mutation
    - No ranking
    - No CTA
    """

    permissions.require_valid_token(authorization)

    result = service.compute_regime_transitions()

    return serializer.serialize(result)
