from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def insert_coin(self, amount: float) -> None: ...

    @abstractmethod
    def select_product(self, product_id: str) -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...

    @abstractmethod
    def refill(self, product_id: str, qty: int) -> None: ...

    def __str__(self):
        return self.__class__.__name__


class IdleState(State):

    def insert_coin(self, amount):
        self.machine.balance += amount
        print(f"Принято {amount}. Баланс: {self.machine.balance}")
        self.machine.set_state(self.machine.has_money)

    def select_product(self, product_id):
        print("Сначала внесите деньги.")

    def cancel(self):
        print("Нечего отменять.")

    def refill(self, product_id, qty):
        print("Пополнение в режиме ожидания недоступно. Используйте MaintenanceMode.")


class HasMoneyState(State):

    def insert_coin(self, amount):
        self.machine.balance += amount
        print(f"Добавлено {amount}. Баланс: {self.machine.balance}")

    def select_product(self, product_id):
        product = self.machine.products.get(product_id)
        if not product:
            print("Товар не найден.")
            return
        if product["stock"] == 0:
            print("Товар закончился.")
            self.machine.set_state(self.machine.out_of_stock)
            return
        if self.machine.balance < product["price"]:
            print(f"Недостаточно средств. Нужно ещё {product['price'] - self.machine.balance:.2f}.")
            return
        self.machine.balance -= product["price"]
        product["stock"] -= 1
        print(f"Выдаётся: {product['name']}. Сдача: {self.machine.balance:.2f}")
        self.machine.balance = 0
        if all(p["stock"] == 0 for p in self.machine.products.values()):
            self.machine.set_state(self.machine.out_of_stock)
        else:
            self.machine.set_state(self.machine.idle)

    def cancel(self):
        print(f"Возврат {self.machine.balance:.2f}.")
        self.machine.balance = 0
        self.machine.set_state(self.machine.idle)

    def refill(self, product_id, qty):
        print("Сначала отмените транзакцию.")


class OutOfStockState(State):

    def insert_coin(self, amount):
        print(f"Товаров нет. Монета {amount} возвращена.")

    def select_product(self, product_id):
        print("Товаров нет.")

    def cancel(self):
        if self.machine.balance > 0:
            print(f"Возврат {self.machine.balance:.2f}.")
            self.machine.balance = 0

    def refill(self, product_id, qty):
        print("Пополнение в OutOfStock недоступно. Используйте MaintenanceMode.")



class MaintenanceState(State):
    """
    Режим обслуживания — добавлен без изменения других классов (OCP).
    Только в этом состоянии можно пополнять товары.
    """

    def insert_coin(self, amount):
        print("Автомат на обслуживании. Монета возвращена.")

    def select_product(self, product_id):
        print("Автомат на обслуживании.")

    def cancel(self):
        print("Выход из режима обслуживания.")
        if all(p["stock"] == 0 for p in self.machine.products.values()):
            self.machine.set_state(self.machine.out_of_stock)
        else:
            self.machine.set_state(self.machine.idle)

    def refill(self, product_id, qty):
        product = self.machine.products.get(product_id)
        if not product:
            print(f"Товар {product_id} не найден.")
            return
        product["stock"] += qty
        print(f"Пополнено: {product['name']} +{qty} шт. Остаток: {product['stock']}")