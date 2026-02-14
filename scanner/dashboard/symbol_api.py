from fastapi import APIRouter, Security, HTTPException
from fastapi.security import APIKeyHeader

from scanner.dashboard.symbol_service import SymbolStateService
from scanner.dashboard.symbol_serializer import SymbolStateSerializer
from scanner.storage.event_repository import EventRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (in-memory binding)
# ----------------------------

event_repo = EventRepository()
observation_manager = ObservationLifecycleManager()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

symbol_service = SymbolStateService(
    event_repo=event_repo,
    observation_manager=observation_manager,
)

serializer = SymbolStateSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(prefix="/symbol", tags=["Symbol"])


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("/{symbol}")
def get_symbol_state(
    symbol: str,
    authorization: str = Security(api_key_header),
):
    """
    Read-only symbol snapshot endpoint.

    Returns:
    - event_count
    - latest_event
    - observation_count

    No scan trigger.
    No mutation.
    """

    permissions.require_valid_token(authorization)

    if not symbol or not symbol.isalnum():
        raise HTTPException(status_code=400, detail="INVALID_SYMBOL")

    state = symbol_service.get_symbol_state(symbol.upper())

    return serializer.serialize(state)
