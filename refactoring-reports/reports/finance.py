from .base import AbstractReportGenerator


class FinanceReport(AbstractReportGenerator):
    def get_title(self):
        return "=== FINANCE REPORT ==="

    def process_data(self, data):
        result = []
        total = 0

        for f in data:
            result.append(f"{f['source']}: {f['value']}")
            total += f["value"]

        result.append(f"Profit: {total}")
        return result