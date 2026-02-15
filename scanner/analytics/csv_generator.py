import csv
from io import StringIO
from typing import List, Dict


class CSVGenerator:
    """
    Deterministic CSV generator.
    No formatting logic.
    No enrichment.
    """

    @staticmethod
    def generate(dataset: List[Dict]) -> str:
        if not dataset:
            return ""

        output = StringIO()

        fieldnames = list(dataset[0].keys())

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for row in dataset:
            writer.writerow(row)

        return output.getvalue()
