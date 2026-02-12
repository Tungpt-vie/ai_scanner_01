from datetime import datetime

from scanner.governance.user_model import User, UserStatus
from scanner.governance.user_repository import UserRepository
from scanner.governance.lifecycle_manager import LifecycleManager
from scanner.governance.delivery_guard import DeliveryGuard
from scanner.governance.audit_logger import AuditLogger


# 1️⃣ Setup
repo = UserRepository()
lifecycle = LifecycleManager(repo)
delivery_guard = DeliveryGuard(repo)
audit = AuditLogger()


# 2️⃣ Create user (default PENDING)
user = User(
    user_id="u1",
    email="test@example.com",
    created_at=datetime.utcnow(),
)

repo.add(user)

print("Initial Status:", user.status.value)


# 3️⃣ Delivery should be blocked (PENDING)
print("Delivery Allowed (PENDING):", delivery_guard.allow_delivery("u1"))


# 4️⃣ Activate user
old_status = user.status
timestamp = lifecycle.activate("u1")
new_status = user.status

audit.log_transition("u1", old_status, new_status, timestamp)

print("After Activate:", user.status.value)
print("Delivery Allowed (ACTIVE):", delivery_guard.allow_delivery("u1"))


# 5️⃣ Suspend user
old_status = user.status
timestamp = lifecycle.suspend("u1")
new_status = user.status

audit.log_transition("u1", old_status, new_status, timestamp)

print("After Suspend:", user.status.value)
print("Delivery Allowed (SUSPENDED):", delivery_guard.allow_delivery("u1"))


# 6️⃣ Reactivate user
old_status = user.status
timestamp = lifecycle.activate("u1")
new_status = user.status

audit.log_transition("u1", old_status, new_status, timestamp)

print("After Reactivate:", user.status.value)


# 7️⃣ Cancel user
old_status = user.status
timestamp = lifecycle.cancel("u1")
new_status = user.status

audit.log_transition("u1", old_status, new_status, timestamp)

print("After Cancel:", user.status.value)
print("Delivery Allowed (CANCELLED):", delivery_guard.allow_delivery("u1"))


# 8️⃣ Invalid transition test (should raise error)
try:
    lifecycle.activate("u1")
except Exception as e:
    print("Invalid Transition Blocked:", str(e))


# 9️⃣ Print audit logs
print("\nAudit Logs:")
for log in audit.get_logs():
    print(log)
