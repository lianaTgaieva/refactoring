from abc import ABC, abstractmethod


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: dict) -> dict:
        ...


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self._orders: list[dict] = []

    def save(self, order: dict) -> dict:
        order = {**order, "id": len(self._orders) + 1}
        self._orders.append(order)
        return order

    @property
    def orders(self) -> list[dict]:
        return list(self._orders)


class DbOrderRepository(OrderRepository):

    def __init__(self, db_conn, orders: list):
        self._db = db_conn
        self._orders = orders

    def save(self, order: dict) -> dict:
        order = {**order, "id": len(self._orders) + 1}
        self._orders.append(order)
        self._db.execute(f"INSERT INTO orders VALUES ({order})")
        return order