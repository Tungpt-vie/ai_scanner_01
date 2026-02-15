from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.analytics.psi_service import PSIService
from scanner.analytics.psi_serializer import PSISerializer
from scanner.storage.event_repository import EventRepository
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


event_repository = EventRepository()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

service = PSIService(event_repository)
serializer = PSISerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="/analytics/pattern-stability",
    tags=["Analytics"]
)


@router.get("")
def get_pattern_stability(
    authorization: str = Security(api_key_header),
):
    permissions.require_valid_token(authorization)

    result = service.compute()

    return serializer.serialize(result)
