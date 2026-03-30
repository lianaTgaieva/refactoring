from reports.sales import SalesReport
from reports.inventory import InventoryReport
from reports.finance import FinanceReport

from strategies.formatters import TextFormatter, HTMLFormatter, CSVFormatter
from handlers.handlers import LoggerHandler, EmailHandler, ArchiveHandler

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def build_chain():
    return LoggerHandler(EmailHandler(ArchiveHandler()))


def test_sales_report():
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    report = SalesReport(TextFormatter(), build_chain())

    result = report.generate(data)

    assert "SALES REPORT" in result
    assert "Total: 300" in result


def test_inventory_report():
    data = [{"name": "Item1", "stock": 5}]
    report = InventoryReport(TextFormatter(), build_chain())

    result = report.generate(data)

    assert "Item1: 5 units" in result


def test_finance_report():
    data = [{"source": "A", "value": 300}]
    report = FinanceReport(TextFormatter(), build_chain())

    result = report.generate(data)

    assert "Profit: 300" in result


def test_empty_data():
    report = SalesReport(TextFormatter(), build_chain())

    result = report.generate([])

    assert "No data" in result


def test_html_format():
    data = [{"id": 1, "amount": 50}]
    report = SalesReport(HTMLFormatter(), build_chain())

    result = report.generate(data)

    assert "<br>" in result


def test_csv_format():
    data = [{"id": 1, "amount": 50}]
    report = SalesReport(CSVFormatter(), build_chain())

    result = report.generate(data)

    assert "," in result