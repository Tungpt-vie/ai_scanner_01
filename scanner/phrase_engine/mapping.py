"""
LOCKED Phrase ↔ Measurement Mapping

Rules:
- One phrase corresponds to one measurable condition.
- No free-text interpretation.
- No subjective adjectives.
- No CTA language.
"""


PHRASE_MAPPING = {
    # RSI conditions
    "RSI_HIGH": {
        "condition": "rsi > 70",
        "description": "RSI above 70"
    },
    "RSI_LOW": {
        "condition": "rsi < 30",
        "description": "RSI below 30"
    },

    # Volume conditions
    "VOLUME_EXPANSION": {
        "condition": "volume_ratio > 1.5",
        "description": "Volume exceeds 1.5x recent average"
    },
    "VOLUME_CONTRACTION": {
        "condition": "volume_ratio < 0.7",
        "description": "Volume below 0.7x recent average"
    },

    # Structure conditions
    "STRUCTURE_FRESH": {
        "condition": "structure_age < 3",
        "description": "Recent structural high within 3 bars"
    },
    "STRUCTURE_MATURE": {
        "condition": "structure_age >= 3",
        "description": "Structure established for at least 3 bars"
    },

    # Regime states
    "REGIME_TRENDING": {
        "condition": "regime == TRENDING",
        "description": "Market regime: Trending"
    },
    "REGIME_RANGING": {
        "condition": "regime == RANGING",
        "description": "Market regime: Ranging"
    },
    "REGIME_VOLATILE": {
        "condition": "regime == VOLATILE",
        "description": "Market regime: Volatile"
    },
    "REGIME_COMPRESSION": {
        "condition": "regime == COMPRESSION",
        "description": "Market regime: Compression"
    },
}
