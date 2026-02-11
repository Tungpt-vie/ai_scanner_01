from scanner.phrase_engine.language import contains_forbidden_language


class PhraseLint:
    """
    Lint engine for phrase validation.

    Rules:
    - If forbidden language detected → DROP silently
    - No logging
    - No warning
    - No modification
    """

    def validate(self, text: str) -> bool:
        """
        Return True if text is allowed.
        Return False if violation detected.
        """

        if not text:
            return False

        if contains_forbidden_language(text):
            return False

        return True
