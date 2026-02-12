from datetime import datetime

from scanner.governance.user_model import User
from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_model import Admin, AdminRole
from scanner.governance.admin_repository import AdminRepository
from scanner.governance.approval_service import ApprovalService
from scanner.governance.command_handler import AdminCommandHandler
from scanner.governance.audit_logger import AuditLogger


# 1️⃣ Setup repositories and services
user_repo = UserRepository()
admin_repo = AdminRepository()
audit_logger = AuditLogger()

approval_service = ApprovalService(
    admin_repo=admin_repo,
    user_repo=user_repo,
    audit_logger=audit_logger,
)

command_handler = AdminCommandHandler(approval_service)


# 2️⃣ Create user (PENDING)
user = User(
    user_id="u1",
    email="user@test.com",
    created_at=datetime.utcnow(),
)
user_repo.add(user)

print("Initial User Status:", user.status.value)


# 3️⃣ Create admins
super_admin = Admin(
    admin_id="a1",
    email="super@test.com",
    role=AdminRole.SUPER_ADMIN,
    created_at=datetime.utcnow(),
)

operator_admin = Admin(
    admin_id="a2",
    email="operator@test.com",
    role=AdminRole.OPERATOR,
    created_at=datetime.utcnow(),
)

auditor_admin = Admin(
    admin_id="a3",
    email="auditor@test.com",
    role=AdminRole.AUDITOR,
    created_at=datetime.utcnow(),
)

admin_repo.add(super_admin)
admin_repo.add(operator_admin)
admin_repo.add(auditor_admin)


# 4️⃣ Auditor tries to approve (should fail)
try:
    command_handler.handle("APPROVE_USER", "a3", "u1")
except Exception as e:
    print("Auditor Approval Blocked:", str(e))


# 5️⃣ Operator approves user
timestamp = command_handler.handle("APPROVE_USER", "a2", "u1")
print("After Operator Approval:", user.status.value)


# 6️⃣ Super admin bans user
timestamp = command_handler.handle("BAN_USER", "a1", "u1")
print("After Super Admin Ban:", user.status.value)


# 7️⃣ Operator tries to ban (should fail)
user2 = User(
    user_id="u2",
    email="user2@test.com",
    created_at=datetime.utcnow(),
)
user_repo.add(user2)

# First approve user2
command_handler.handle("APPROVE_USER", "a2", "u2")

try:
    command_handler.handle("BAN_USER", "a2", "u2")
except Exception as e:
    print("Operator Ban Blocked:", str(e))


# 8️⃣ Print audit logs
print("\nAudit Logs:")
for log in audit_logger.get_logs():
    print(log)
