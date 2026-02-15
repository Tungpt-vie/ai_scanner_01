from typing import Dict, Optional


class MarketRegimeSerializer:
    """
    Safe serializer for Market Regime Dashboard.

    Rules:
    - No internal cache exposure
    - No recompute logic
    - No CTA
    - Deterministic output
    """

    def serialize(self, regime_data: Dict, metadata: Optional[Dict] = None) -> Dict:
        response = {
            "current_regime": regime_data.get("regime"),
            "source": regime_data.get("source"),
        }

        if metadata:
            # Only allow safe metadata keys
            safe_metadata = {
                k: v for k, v in metadata.items()
                if isinstance(k, str)
            }
            response["metadata"] = safe_metadata

        return response
