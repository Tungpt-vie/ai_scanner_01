from fastapi import APIRouter, Security, Query
from fastapi.security import APIKeyHeader
from typing import Optional

from scanner.dashboard.observation_history_service import ObservationHistoryService
from scanner.dashboard.observation_history_serializer import ObservationHistorySerializer
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (in-memory binding)
# ----------------------------

observation_manager = ObservationLifecycleManager()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

history_service = ObservationHistoryService(observation_manager)
serializer = ObservationHistorySerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(prefix="/history", tags=["Observation History"])


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_closed_history(
    authorization: str = Security(api_key_header),
    descending: bool = Query(True),
    limit: Optional[int] = Query(None),
):
    """
    Return CLOSED observation history only.

    Immutable.
    No reopen.
    No mutation.
    """

    permissions.require_valid_token(authorization)

    history = history_service.get_closed_history(
        descending=descending,
        limit=limit,
    )

    return serializer.serialize_list(history)
