import smtplib
from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send_order_confirmation(self, email: str, order: dict) -> None:
        ...


class EmailNotifier(Notifier):

    SENDER = "shop@store.com"

    def __init__(self, smtp_host: str, smtp_port: int):
        self._host = smtp_host
        self._port = smtp_port

    def send_order_confirmation(self, email: str, order: dict) -> None:
        message = (
            f"Заказ #{order['id']} подтверждён. "
            f"Итого: {order['total']:.2f}"
        )
        server = smtplib.SMTP(self._host, self._port)
        try:
            server.sendmail(self.SENDER, email, message)
        finally:
            server.quit()


class ConsoleNotifier(Notifier):

    def send_order_confirmation(self, email: str, order: dict) -> None:
        print(
            f"[NOTIFIER] → {email}: "
            f"Заказ #{order['id']} подтверждён, "
            f"итого {order['total']:.2f}"
        )