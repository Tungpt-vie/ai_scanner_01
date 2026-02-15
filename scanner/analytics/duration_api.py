from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.analytics.duration_service import DurationService
from scanner.analytics.duration_serializer import DurationSerializer
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# INIT (read-only)
observation_manager = ObservationLifecycleManager()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

service = DurationService(observation_manager)
serializer = DurationSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="/analytics/observation-duration",
    tags=["Analytics"]
)


@router.get("")
def get_observation_duration(
    authorization: str = Security(api_key_header),
):
    permissions.require_valid_token(authorization)

    result = service.compute()

    return serializer.serialize(result)
