import time
import hashlib

from scanner.security.rate_limiter import RateLimiter
from scanner.security.auth_guard import AuthGuard
from scanner.security.input_validator import InputValidator
from scanner.security.webhook_guard import WebhookGuard
from scanner.security.resource_guard import ResourceGuard
from scanner.security.security_logger import SecurityLogger

from scanner.governance.user_repository import UserRepository
from scanner.governance.admin_repository import AdminRepository
from scanner.governance.user_model import User
from scanner.governance.admin_model import Admin, AdminRole
from datetime import datetime


print("=== RATE LIMIT TEST ===")
rate_limiter = RateLimiter(max_requests=2, window_seconds=2)

print(rate_limiter.allow("u1"))  # True
print(rate_limiter.allow("u1"))  # True
print(rate_limiter.allow("u1"))  # False (limit reached)

time.sleep(3)
print(rate_limiter.allow("u1"))  # True (window reset)


print("\n=== AUTH GUARD TEST ===")
user_repo = UserRepository()
admin_repo = AdminRepository()

user_repo.add(User("u1", "u@test.com", datetime.utcnow()))
admin_repo.add(Admin("a1", "a@test.com", AdminRole.SUPER_ADMIN, datetime.utcnow()))

auth = AuthGuard(admin_repo, user_repo)

print(auth.validate_token("TOKEN_ABC"))  # True
print(auth.validate_token("INVALID"))    # False

auth.require_user("u1")  # should pass

try:
    auth.require_admin("unknown")
except Exception as e:
    print("Admin check blocked:", str(e))


print("\n=== INPUT VALIDATOR TEST ===")
validator = InputValidator()

print(validator.validate_symbol(" vcb "))  # VCB

try:
    validator.validate_symbol("!!!")
except Exception as e:
    print("Invalid symbol blocked:", str(e))

payload = {"symbol": "VCB", "type": "OBS"}
print(validator.validate_event_payload(payload))  # True


print("\n=== WEBHOOK GUARD TEST ===")
secret = "SECRET"
rl = RateLimiter(max_requests=5, window_seconds=10)
webhook = WebhookGuard(secret, rl)

payload = {"symbol": "VCB", "type": "OBS"}

normalized = "&".join(f"{k}={v}" for k, v in sorted(payload.items()))
signature = hashlib.sha256((secret + normalized).encode()).hexdigest()

print("Signature valid:", webhook.verify_signature(payload, signature))
print("Signature replay first:", webhook.check_replay(signature))
print("Signature replay second:", webhook.check_replay(signature))  # False


print("\n=== RESOURCE GUARD TEST ===")
resource = ResourceGuard(max_events=1, max_deliveries=1, max_observations=1)

resource.validate_all({
    "events": 1,
    "deliveries": 1,
    "observations": 1
})

try:
    resource.validate_all({"events": 2})
except Exception as e:
    print("Event capacity blocked:", str(e))


print("\n=== SECURITY LOGGER TEST ===")
logger = SecurityLogger()
logger.log_event("RATE_LIMIT_BLOCK", "u1", {"ip": "127.0.0.1"})
logger.log_event("INVALID_TOKEN", "u2")

logs = logger.get_logs()
print("Log Count:", len(logs))
print("First Log:", logs[0])
