from datetime import datetime

from scanner.governance.user_model import User, UserStatus
from scanner.governance.user_repository import UserRepository
from scanner.governance.subscription_model import UserSubscription, SubscriptionTier
from scanner.governance.subscription_repository import SubscriptionRepository
from scanner.governance.watchlist_model import UserWatchlist
from scanner.governance.watchlist_repository import WatchlistRepository
from scanner.governance.delivery_router import DeliveryRouter


# 1️⃣ Setup repositories
user_repo = UserRepository()
sub_repo = SubscriptionRepository()
watch_repo = WatchlistRepository()

router = DeliveryRouter(user_repo, sub_repo, watch_repo)


# 2️⃣ Create ACTIVE user
user = User(
    user_id="u1",
    email="user@test.com",
    created_at=datetime.utcnow(),
)
user.status = UserStatus.ACTIVE
user_repo.add(user)


# 3️⃣ Create FREE subscription
subscription = UserSubscription(
    user_id="u1",
    created_at=datetime.utcnow(),
)
sub_repo.add(subscription)


# 4️⃣ Create watchlist and add symbol VCB
watchlist = UserWatchlist(user_id="u1")
watchlist.add_symbol("VCB")
watch_repo.add(watchlist)


# 🔎 FREE tier tests
print("FREE - VCB (should True):", router.allow_delivery("u1", "VCB"))
print("FREE - FPT (should False):", router.allow_delivery("u1", "FPT"))


# 5️⃣ Upgrade to STANDARD
subscription.upgrade(SubscriptionTier.STANDARD)

print("STANDARD - FPT (should True):", router.allow_delivery("u1", "FPT"))


# 6️⃣ Downgrade to FREE again
subscription.downgrade_to_free()

print("FREE again - FPT (should False):", router.allow_delivery("u1", "FPT"))


# 7️⃣ PRO tier
subscription.upgrade(SubscriptionTier.PRO)

print("PRO - Any symbol (should True):", router.allow_delivery("u1", "AAA"))


# 8️⃣ Lifecycle block test
user.status = UserStatus.SUSPENDED
print("SUSPENDED - PRO (should False):", router.allow_delivery("u1", "VCB"))


# 9️⃣ Missing subscription test
user2 = User(
    user_id="u2",
    email="user2@test.com",
    created_at=datetime.utcnow(),
)
user2.status = UserStatus.ACTIVE
user_repo.add(user2)

try:
    router.allow_delivery("u2", "VCB")
except Exception as e:
    print("Missing Subscription Blocked:", str(e))
