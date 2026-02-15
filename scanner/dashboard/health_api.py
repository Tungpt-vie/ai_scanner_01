from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.dashboard.health_service import SystemHealthService
from scanner.dashboard.health_serializer import SystemHealthSerializer
from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.optimization.regime_cache import RegimeCache
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (in-memory binding only)
# ----------------------------

event_repo = EventRepository()
delivery_repo = DeliveryRepository()
observation_manager = ObservationLifecycleManager()
regime_cache = RegimeCache()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

health_service = SystemHealthService(
    event_repo=event_repo,
    delivery_repo=delivery_repo,
    observation_manager=observation_manager,
    regime_cache=regime_cache,
)

serializer = SystemHealthSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(prefix="/health", tags=["System Health"])


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_system_health(
    authorization: str = Security(api_key_header),
):
    """
    Read-only system health endpoint.

    - No scan trigger
    - No mutation
    - No recompute
    - Deterministic snapshot
    """

    permissions.require_valid_token(authorization)

    snapshot = health_service.get_health_snapshot()

    return serializer.serialize(snapshot)
