class InventoryManager:

    def __init__(self, inventory: dict):
        self._inventory = inventory

    def reserve(self, items: dict) -> None:
        for item_id, qty in items.items():
            self._inventory[item_id]["stock"] -= qty