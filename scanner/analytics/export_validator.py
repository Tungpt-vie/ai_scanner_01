from typing import List


class ExportValidator:
    """
    PRO-only export validator.

    - No mutation
    - Read-only
    - Dataset size guard
    """

    MAX_EXPORT_ROWS = 5000  # hard limit

    @staticmethod
    def validate_pro_access(user_role: str) -> None:
        if user_role != "PRO":
            raise PermissionError("EXPORT_PRO_ONLY")

    @staticmethod
    def validate_row_limit(dataset: List[dict]) -> None:
        if len(dataset) > ExportValidator.MAX_EXPORT_ROWS:
            raise ValueError("EXPORT_LIMIT_EXCEEDED")
