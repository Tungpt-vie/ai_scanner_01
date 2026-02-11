"""
Strict language enforcement module.

Purpose:
- Block CTA (call-to-action) wording
- Block BUY / SELL directives
- Block forecasting language
- Block emotional bias words
- Allow descriptive technical phrasing only
"""


FORBIDDEN_KEYWORDS = [
    # Direct actions
    "buy",
    "sell",
    "enter",
    "exit",
    "long",
    "short",
    "take position",
    "accumulate",
    "distribute",

    # Advisory tone
    "should",
    "must",
    "recommend",
    "advise",
    "consider buying",
    "consider selling",

    # Forecasting / predictive
    "will rise",
    "will fall",
    "expected to",
    "likely to",
    "guarantee",
    "predict",

    # Emotional / bias
    "bullish",
    "bearish",
    "strong opportunity",
    "high probability",
    "safe",
    "certain",
]


def contains_forbidden_language(text: str) -> bool:
    """
    Check if rendered text contains any forbidden keyword.
    Case-insensitive match.
    """

    lower_text = text.lower()

    for word in FORBIDDEN_KEYWORDS:
        if word in lower_text:
            return True

    return False
