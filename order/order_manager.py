from validators import UserValidator, InventoryValidator
from pricing import PriceCalculator, get_discount_strategy
from inventory import InventoryManager
from repository import OrderRepository
from notifier import Notifier


class OrderManager:
    def __init__(
        self,
        users: dict,
        inventory: dict,
        price_calculator: PriceCalculator,
        order_repository: OrderRepository,
        notifier: Notifier,
    ):
        self._users = users
        self._user_validator = UserValidator(users)
        self._inventory_validator = InventoryValidator(inventory)
        self._inventory_manager = InventoryManager(inventory)
        self._price_calculator = price_calculator
        self._repository = order_repository
        self._notifier = notifier

    def create_order(self, user_id: str, items: dict, promo_code: str | None = None) -> dict:
        self._user_validator.validate(user_id)
        self._inventory_validator.validate(items)

        discount = get_discount_strategy(promo_code)
        from inventory import InventoryManager
        inventory_snapshot = self._inventory_manager._inventory  # read-only access
        total = self._price_calculator.calculate(items, inventory_snapshot, discount)

        self._inventory_manager.reserve(items)

        order = self._repository.save({
            "user": user_id,
            "items": items,
            "total": total,
            "status": "new",
        })

        self._notifier.send_order_confirmation(
            self._users[user_id]["email"], order
        )

        return order