from scanner.governance.user_repository import UserRepository
from scanner.governance.subscription_repository import SubscriptionRepository
from scanner.governance.watchlist_repository import WatchlistRepository
from scanner.governance.user_model import UserStatus
from scanner.governance.subscription_model import SubscriptionTier


class DeliveryGuard:
    """
    Delivery enforcement bridge.

    Responsibilities:
    - Enforce lifecycle ACTIVE
    - Enforce subscription existence
    - Enforce FREE watchlist restriction
    - Scanner-agnostic
    - Deterministic
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

    def allow(self, user_id: str, symbol: str) -> bool:
        """
        Determine if delivery is allowed.
        """

        # 1️⃣ Lifecycle check
        user = self.user_repo.get(user_id)
        if user.status != UserStatus.ACTIVE:
            return False

        # 2️⃣ Subscription check
        subscription = self.subscription_repo.get(user_id)

        # 3️⃣ FREE tier → enforce watchlist
        if subscription.tier == SubscriptionTier.FREE:
            watchlist = self.watchlist_repo.get(user_id)
            return watchlist.has_symbol(symbol)

        # 4️⃣ STANDARD & PRO → allow
        if subscription.tier in (
            SubscriptionTier.STANDARD,
            SubscriptionTier.PRO,
        ):
            return True

        return False
