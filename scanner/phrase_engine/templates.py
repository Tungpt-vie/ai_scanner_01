"""
Render-only templates.

Rules:
- No BUY / SELL
- No advice
- No emotional wording
- No forecasting
- Pure structural description
"""


TEMPLATES = {

    "BASE_STRUCTURE": "{symbol} | Regime: {regime} | State: {ta_state}",

    "RSI_HIGH": "RSI above 70 indicates elevated momentum readings.",
    "RSI_LOW": "RSI below 30 indicates compressed momentum readings.",

    "VOLUME_EXPANSION": "Volume exceeds 1.5 times the recent average.",
    "VOLUME_CONTRACTION": "Volume remains below 0.7 times the recent average.",

    "STRUCTURE_FRESH": "Recent structural high formed within the last 3 bars.",
    "STRUCTURE_MATURE": "Structural formation sustained for at least 3 bars.",

    "REGIME_TRENDING": "Market regime classified as trending.",
    "REGIME_RANGING": "Market regime classified as ranging.",
    "REGIME_VOLATILE": "Market regime classified as volatile.",
    "REGIME_COMPRESSION": "Market regime classified as compression.",

    "FOOTER": "This output is descriptive and contains no action directive."
}
