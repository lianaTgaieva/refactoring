class UserValidator:

    def __init__(self, users: dict):
        self._users = users

    def validate(self, user_id: str) -> None:
        if user_id not in self._users:
            raise ValueError(f"Пользователь {user_id} не найден")
        if self._users[user_id].get("banned"):
            raise PermissionError(f"Пользователь {user_id} заблокирован")


class InventoryValidator:

    def __init__(self, inventory: dict):
        self._inventory = inventory

    def validate(self, items: dict) -> None:
        for item_id, qty in items.items():
            if item_id not in self._inventory:
                raise ValueError(f"Товар {item_id} не найден")
            if self._inventory[item_id]["stock"] < qty:
                raise ValueError(f"Недостаточно товара {item_id} на складе")