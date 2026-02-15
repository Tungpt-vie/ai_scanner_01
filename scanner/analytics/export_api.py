from fastapi import APIRouter, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.responses import PlainTextResponse

from scanner.analytics.export_service import ExportService
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

service = ExportService(event_repository)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter(
    prefix="/analytics/export",
    tags=["Analytics"]
)


@router.get("/events", response_class=PlainTextResponse)
def export_events(
    authorization: str = Security(api_key_header),
):
    permissions.require_valid_token(authorization)

    # In real system, role fetched from auth context
    user_role = "PRO"

    try:
        csv_data = service.export_events(user_role)
        return csv_data
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
