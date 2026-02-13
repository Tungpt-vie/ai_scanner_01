from datetime import datetime
import time

from scanner.governance.user_model import User, UserStatus
from scanner.governance.user_repository import UserRepository
from scanner.governance.subscription_model import UserSubscription, SubscriptionTier
from scanner.governance.subscription_repository import SubscriptionRepository
from scanner.governance.watchlist_model import UserWatchlist
from scanner.governance.watchlist_repository import WatchlistRepository

from scanner.delivery.delivery_guard import DeliveryGuard
from scanner.delivery.cooldown_manager import CooldownManager
from scanner.delivery.watchlist_router import WatchlistRouter
from scanner.delivery.dispatcher import Dispatcher


# 1️⃣ Setup repositories
user_repo = UserRepository()
sub_repo = SubscriptionRepository()
watch_repo = WatchlistRepository()

# 2️⃣ Create users
u1 = User("u1", "u1@test.com", datetime.utcnow())
u1.status = UserStatus.ACTIVE
user_repo.add(u1)

u2 = User("u2", "u2@test.com", datetime.utcnow())
u2.status = UserStatus.ACTIVE
user_repo.add(u2)

u3 = User("u3", "u3@test.com", datetime.utcnow())
u3.status = UserStatus.SUSPENDED
user_repo.add(u3)


# 3️⃣ Subscriptions
sub_repo.add(UserSubscription("u1", datetime.utcnow()))  # FREE
sub_repo.add(UserSubscription("u2", datetime.utcnow()))  # FREE
sub_repo.add(UserSubscription("u3", datetime.utcnow()))  # FREE


# 4️⃣ Watchlists
w1 = UserWatchlist("u1")
w1.add_symbol("VCB")
watch_repo.add(w1)

w2 = UserWatchlist("u2")
w2.add_symbol("FPT")
watch_repo.add(w2)

w3 = UserWatchlist("u3")
w3.add_symbol("VCB")
watch_repo.add(w3)


# 5️⃣ Build delivery system
guard = DeliveryGuard(user_repo, sub_repo, watch_repo)
cooldown = CooldownManager(cooldown_seconds=2)
router = WatchlistRouter(watch_repo)
dispatcher = Dispatcher(guard, cooldown)


# 🔎 Resolve users for VCB
targets = router.resolve_users_for_symbol("VCB")
print("Watchlist Targets (VCB):", targets)

# 🔎 Dispatch first time
result1 = dispatcher.dispatch(targets, "VCB")
print("First Dispatch Result:", result1)

# 🔎 Immediate second dispatch (should be cooldown blocked)
result2 = dispatcher.dispatch(targets, "VCB")
print("Second Dispatch (Cooldown Block):", result2)

# 🔎 Wait for cooldown expiry
time.sleep(3)

result3 = dispatcher.dispatch(targets, "VCB")
print("After Cooldown Dispatch:", result3)

# 🔎 Upgrade u2 to STANDARD and test routing
sub_repo.get("u2").upgrade(SubscriptionTier.STANDARD)

# Directly dispatch FPT
result4 = dispatcher.dispatch(["u2"], "FPT")
print("STANDARD user dispatch (FPT):", result4)

# 🔎 Suspended user should not receive
result5 = dispatcher.dispatch(["u3"], "VCB")
print("Suspended user dispatch:", result5)
