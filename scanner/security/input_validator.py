from typing import Dict


class InputValidator:
    """
    Strict input validation layer.

    Rules:
    - No silent coercion
    - No auto-correction
    - Deterministic validation
    - Raise explicit error on invalid input
    """

    def validate_symbol(self, symbol: str) -> str:
        """
        Validate stock symbol format.
        """

        if not isinstance(symbol, str):
            raise ValueError("INVALID_SYMBOL_TYPE")

        normalized = symbol.strip().upper()

        if not normalized:
            raise ValueError("EMPTY_SYMBOL")

        if not normalized.isalnum():
            raise ValueError("INVALID_SYMBOL_FORMAT")

        if len(normalized) > 10:
            raise ValueError("SYMBOL_TOO_LONG")

        return normalized

    def validate_event_payload(self, payload: Dict):
        """
        Validate event payload structure.
        Required keys:
        - symbol (str)
        - type (str)
        """

        if not isinstance(payload, dict):
            raise ValueError("INVALID_PAYLOAD_TYPE")

        if "symbol" not in payload:
            raise ValueError("MISSING_SYMBOL")

        if "type" not in payload:
            raise ValueError("MISSING_TYPE")

        if not isinstance(payload["symbol"], str):
            raise ValueError("INVALID_SYMBOL_FIELD")

        if not isinstance(payload["type"], str):
            raise ValueError("INVALID_TYPE_FIELD")

        return True
