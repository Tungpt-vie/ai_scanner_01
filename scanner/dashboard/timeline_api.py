from fastapi import APIRouter, Security, Query, HTTPException
from fastapi.security import APIKeyHeader
from typing import Optional
from datetime import datetime

from scanner.dashboard.timeline_service import TimelineService
from scanner.dashboard.timeline_serializer import TimelineSerializer
from scanner.storage.event_repository import EventRepository
from scanner.security.auth_guard import AuthGuard
from scanner.dashboard.permissions import DashboardPermission
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository


# ----------------------------
# INIT (in-memory binding)
# ----------------------------

event_repo = EventRepository()
user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)
permissions = DashboardPermission(auth_guard)

timeline_service = TimelineService(event_repo)
serializer = TimelineSerializer()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(prefix="/timeline", tags=["Timeline"])


# ----------------------------
# ENDPOINT
# ----------------------------

@router.get("")
def get_timeline(
    authorization: str = Security(api_key_header),
    symbol: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    descending: bool = Query(True),
):
    """
    Immutable timeline query endpoint.

    Filters:
    - symbol
    - start_time (ISO format)
    - end_time (ISO format)
    - descending (default True)
    """

    permissions.require_valid_token(authorization)

    try:
        parsed_start = datetime.fromisoformat(start_time) if start_time else None
        parsed_end = datetime.fromisoformat(end_time) if end_time else None
    except Exception:
        raise HTTPException(status_code=400, detail="INVALID_TIME_FORMAT")

    events = timeline_service.get_timeline(
        symbol=symbol,
        start_time=parsed_start,
        end_time=parsed_end,
        descending=descending,
    )

    return serializer.serialize_list(events)
