from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class SubscriptionTier(Enum):
    """
    Strict subscription tiers.
    """

    FREE = "FREE"
    STANDARD = "STANDARD"
    PRO = "PRO"


@dataclass
class UserSubscription:
    """
    Subscription model.

    Rules:
    - Default tier is FREE
    - No implicit upgrade
    - Independent from lifecycle
    """

    user_id: str
    created_at: datetime
    tier: SubscriptionTier = SubscriptionTier.FREE

    def upgrade(self, new_tier: SubscriptionTier):
        if new_tier == self.tier:
            raise ValueError("NO_TIER_CHANGE")

        if new_tier == SubscriptionTier.FREE:
            raise ValueError("INVALID_DOWNGRADE_TO_FREE")

        self.tier = new_tier

    def downgrade_to_free(self):
        self.tier = SubscriptionTier.FREE
