from abc import ABC, abstractmethod
from datetime import datetime


class AbstractReportGenerator(ABC):
    def __init__(self, formatter, handler_chain):
        self.formatter = formatter
        self.handler_chain = handler_chain

    def generate(self, data):
        report = []

        report.append(self.get_title())
        report.append(self.get_period())

        if not data:
            report.append("No data")
            return self.formatter.format(report)

        report.extend(self.process_data(data))
        report.append(self.get_footer())

        formatted = self.formatter.format(report)

        # Chain of Responsibility
        if self.handler_chain:
            self.handler_chain.handle(formatted)

        return formatted

    @abstractmethod
    def get_title(self):
        pass

    def get_period(self):
        return f"Generated at: {datetime.now()}"

    @abstractmethod
    def process_data(self, data):
        pass

    def get_footer(self):
        return "=== END ==="