class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, report):
        self.process(report)
        if self.next:
            self.next.handle(report)

    def process(self, report):
        pass


class LoggerHandler(Handler):
    def process(self, report):
        print("LOG: report generated")


class EmailHandler(Handler):
    def process(self, report):
        print("EMAIL: report sent")


class ArchiveHandler(Handler):
    def process(self, report):
        print("ARCHIVE: report saved")