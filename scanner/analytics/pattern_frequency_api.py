from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from scanner.analytics.pattern_frequency_service import PatternFrequencyService
from scanner.analytics.pattern_frequency_serializer import PatternFrequencySerializer
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

service = PatternFrequencyService(event_repository)
serializer = PatternFrequencySerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="/analytics/pattern-frequency",
    tags=["Analytics"]
)


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_pattern_frequency(
    authorization: str = Security(api_key_header),
):
    """
    Read-only Pattern Frequency Analytics.

    - No mutation
    - No ranking
    - No performance metrics
    - No CTA
    """

    permissions.require_valid_token(authorization)

    result = service.compute_frequency()

    return serializer.serialize(result)
