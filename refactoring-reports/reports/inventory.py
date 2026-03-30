from .base import AbstractReportGenerator


class InventoryReport(AbstractReportGenerator):
    def get_title(self):
        return "=== INVENTORY REPORT ==="

    def process_data(self, data):
        result = []

        for i in data:
            result.append(f"{i['name']}: {i['stock']} units")

        return result