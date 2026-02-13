import hashlib
from typing import Dict

from scanner.security.rate_limiter import RateLimiter


class WebhookGuard:
    """
    Webhook protection layer.

    Responsibilities:
    - Signature verification (deterministic HMAC-style check)
    - Rate limiting enforcement
    - Basic replay protection stub
    - No scanner mutation
    """

    def __init__(
        self,
        secret_key: str,
        rate_limiter: RateLimiter,
    ):
        self.secret_key = secret_key
        self.rate_limiter = rate_limiter
        self._processed_signatures = set()

    def verify_signature(self, payload: Dict, signature: str) -> bool:
        """
        Deterministic signature verification.

        signature = SHA256(secret_key + sorted_payload_string)
        """

        if not isinstance(signature, str):
            return False

        payload_string = self._normalize_payload(payload)
        expected = hashlib.sha256(
            (self.secret_key + payload_string).encode("utf-8")
        ).hexdigest()

        return signature == expected

    def allow_request(self, key: str) -> bool:
        """
        Apply rate limit by key (IP or webhook ID).
        """
        return self.rate_limiter.allow(key)

    def check_replay(self, signature: str) -> bool:
        """
        Basic replay protection:
        - Reject if same signature already processed
        """

        if signature in self._processed_signatures:
            return False

        self._processed_signatures.add(signature)
        return True

    def _normalize_payload(self, payload: Dict) -> str:
        """
        Deterministic payload normalization.
        """
        items = sorted(payload.items())
        return "&".join(f"{k}={v}" for k, v in items)
