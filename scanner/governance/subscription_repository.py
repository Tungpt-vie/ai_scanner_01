from typing import Dict
from scanner.governance.subscription_model import UserSubscription


class SubscriptionRepository:
    """
    Deterministic in-memory subscription repository.

    Rules:
    - No auto-create on get
    - Explicit add only
    - One subscription per user
    - No implicit upgrade
    """

    def __init__(self):
        self._subscriptions: Dict[str, UserSubscription] = {}

    def add(self, subscription: UserSubscription):
        if subscription.user_id in self._subscriptions:
            raise ValueError("SUBSCRIPTION_ALREADY_EXISTS")
        self._subscriptions[subscription.user_id] = subscription

    def get(self, user_id: str) -> UserSubscription:
        if user_id not in self._subscriptions:
            raise ValueError("SUBSCRIPTION_NOT_FOUND")
        return self._subscriptions[user_id]

    def exists(self, user_id: str) -> bool:
        return user_id in self._subscriptions

    def remove(self, user_id: str):
        if user_id not in self._subscriptions:
            raise ValueError("SUBSCRIPTION_NOT_FOUND")
        del self._subscriptions[user_id]

    def list_all(self):
        return list(self._subscriptions.values())
