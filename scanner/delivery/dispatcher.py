from typing import List
from scanner.delivery.cooldown_manager import CooldownManager
from scanner.delivery.delivery_guard import DeliveryGuard


class Dispatcher:
    """
    Channel-safe dispatch engine.

    Rules:
    - No scanner mutation
    - No cross-user leak
    - Cooldown enforced
    - Idempotent per (user_id, symbol)
    - Deterministic behavior
    """

    def __init__(
        self,
        delivery_guard: DeliveryGuard,
        cooldown_manager: CooldownManager,
    ):
        self.delivery_guard = delivery_guard
        self.cooldown_manager = cooldown_manager

    def dispatch(self, user_ids: List[str], symbol: str) -> List[str]:
        """
        Attempt delivery for list of users.

        Returns list of successfully delivered user_ids.
        """

        delivered = []

        for user_id in user_ids:

            # 1️⃣ Enforce delivery rules
            if not self.delivery_guard.allow(user_id, symbol):
                continue

            # 2️⃣ Enforce cooldown
            if not self.cooldown_manager.can_deliver(user_id, symbol):
                continue

            # 3️⃣ Mark delivered
            self.cooldown_manager.mark_delivered(user_id, symbol)

            delivered.append(user_id)

        return delivered
