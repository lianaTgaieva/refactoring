class TextFormatter:
    def format(self, report):
        return "\n".join(report)


class CSVFormatter:
    def format(self, report):
        return ",".join(report)


class HTMLFormatter:
    def format(self, report):
        return "<br>".join(report)