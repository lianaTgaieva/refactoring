from .base import AbstractReportGenerator


class SalesReport(AbstractReportGenerator):
    def get_title(self):
        return "=== SALES REPORT ==="

    def process_data(self, data):
        result = []
        total = 0

        for s in data:
            result.append(f"{s['id']}: {s['amount']}")
            total += s["amount"]

        result.append(f"Total: {total}")
        return result
        