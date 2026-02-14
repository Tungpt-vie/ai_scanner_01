from fastapi.security import APIKeyHeader
from fastapi import Security

from fastapi import FastAPI, Header, HTTPException
from typing import Optional

from scanner.dashboard.query_service import DashboardQueryService
from scanner.dashboard.serializers import DashboardSerializer
from scanner.dashboard.permissions import DashboardPermission

from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository
from scanner.observation.lifecycle_manager import ObservationLifecycleManager

from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository
from scanner.security.auth_guard import AuthGuard


# ----------------------------
# INIT (in-memory binding)
# ----------------------------

event_repo = EventRepository()
delivery_repo = DeliveryRepository()
observation_manager = ObservationLifecycleManager()

user_repo = UserRepository()
admin_repo = AdminRepository()

auth_guard = AuthGuard(admin_repo, user_repo)

query_service = DashboardQueryService(
    event_repo,
    delivery_repo,
    observation_manager,
)

serializer = DashboardSerializer()
permissions = DashboardPermission(auth_guard)

app = FastAPI(title="AI_SCANNER_01 Dashboard API (Read-Only)")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# ----------------------------
# ENDPOINTS
# ----------------------------

@app.get("/summary")
def get_summary(
    authorization: str = Security(api_key_header)
):

    permissions.require_valid_token(authorization)

    data = query_service.summary()
    return serializer.serialize_summary(data)


@app.get("/events")
def get_events(
    authorization: str = Security(api_key_header)
):

    permissions.require_valid_token(authorization)

    events = query_service.list_events()
    return serializer.serialize_event_list(events)


@app.get("/deliveries")
def get_deliveries(
    authorization: str = Security(api_key_header)
):

    permissions.require_valid_token(authorization)

    deliveries = query_service.list_deliveries()
    return serializer.serialize_delivery_list(deliveries)


@app.get("/observations")
def get_observations(
    authorization: str = Security(api_key_header)
):

    permissions.require_valid_token(authorization)

    observations = query_service.list_observations()
    return serializer.serialize_observation_list(observations)
