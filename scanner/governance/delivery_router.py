from scanner.governance.user_repository import UserRepository
from scanner.governance.subscription_repository import SubscriptionRepository
from scanner.governance.watchlist_repository import WatchlistRepository
from scanner.governance.user_model import UserStatus
from scanner.governance.subscription_model import SubscriptionTier


class DeliveryRouter:
    """
    Delivery routing control layer.

    Rules:
    - Scanner remains independent
    - ACTIVE lifecycle required
    - Subscription tier enforced
    - Watchlist enforced for FREE
    - Deterministic routing
    """

    def __init__(
        self,
        user_repo: UserRepository,
        subscription_repo: SubscriptionRepository,
        watchlist_repo: WatchlistRepository,
    ):
        self.user_repo = user_repo
        self.subscription_repo = subscription_repo
        self.watchlist_repo = watchlist_repo

    def allow_delivery(self, user_id: str, symbol: str) -> bool:
        """
        Determine if event for symbol can be delivered to user.
        """

        # 1️⃣ Lifecycle must be ACTIVE
        user = self.user_repo.get(user_id)
        if user.status != UserStatus.ACTIVE:
            return False

        # 2️⃣ Subscription must exist
        subscription = self.subscription_repo.get(user_id)

        # 3️⃣ FREE tier → only watchlist symbols allowed
        if subscription.tier == SubscriptionTier.FREE:
            watchlist = self.watchlist_repo.get(user_id)
            return watchlist.has_symbol(symbol)

        # 4️⃣ STANDARD tier → all symbols allowed
        if subscription.tier == SubscriptionTier.STANDARD:
            return True

        # 5️⃣ PRO tier → all symbols allowed
        if subscription.tier == SubscriptionTier.PRO:
            return True

        return False
