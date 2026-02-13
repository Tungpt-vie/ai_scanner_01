import hashlib
import json
from typing import Dict


class EventHashGenerator:
    """
    Deterministic event fingerprint generator.

    Rules:
    - No randomness
    - Same input → same hash
    - Order-stable
    - Scanner-agnostic
    """

    def generate(self, event_payload: Dict) -> str:
        """
        Generate SHA256 hash from normalized event payload.
        """

        # Ensure deterministic ordering
        normalized = json.dumps(
            event_payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
