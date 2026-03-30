from states import IdleState, HasMoneyState, OutOfStockState, MaintenanceState


class VendingMachine:
    def __init__(self, products: dict):
        """
        products = {
            'A1': {'name': 'Вода', 'price': 50.0, 'stock': 5},
            ...
        }
        """
        self.products = products
        self.balance = 0.0

        self.idle         = IdleState(self)
        self.has_money    = HasMoneyState(self)
        self.out_of_stock = OutOfStockState(self)
        self.maintenance  = MaintenanceState(self)

        self._state = self.idle


    def insert_coin(self, amount: float):
        self._state.insert_coin(amount)

    def select_product(self, product_id: str):
        self._state.select_product(product_id)

    def cancel(self):
        self._state.cancel()

    def refill(self, product_id: str, qty: int):
        self._state.refill(product_id, qty)

    def enter_maintenance(self):
        print("Переход в режим обслуживания.")
        self.set_state(self.maintenance)


    def set_state(self, state):
        print(f"  [переход: {self._state} → {state}]")
        self._state = state

    @property
    def current_state(self) -> str:
        return str(self._state)