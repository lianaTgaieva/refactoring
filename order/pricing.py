from abc import ABC, abstractmethod


class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        ...


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total


class PercentDiscount(DiscountStrategy):

    def __init__(self, percent: float):
        self._multiplier = 1 - percent / 100

    def apply(self, total: float) -> float:
        return total * self._multiplier


PROMO_STRATEGIES: dict[str | None, DiscountStrategy] = {
    None:       NoDiscount(),
    "SAVE10":   PercentDiscount(10),
    "SAVE20":   PercentDiscount(20),
}


def get_discount_strategy(promo_code: str | None) -> DiscountStrategy:
    return PROMO_STRATEGIES.get(promo_code, NoDiscount())


class PriceCalculator:

    def __init__(self, tax_rate: float):
        self._tax_rate = tax_rate

    def calculate(
        self,
        items: dict,
        inventory: dict,
        discount: DiscountStrategy,
    ) -> float:
        subtotal = sum(
            inventory[item_id]["price"] * qty
            for item_id, qty in items.items()
        )
        subtotal = discount.apply(subtotal)
        return subtotal * (1 + self._tax_rate)