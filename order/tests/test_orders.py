import pytest
from unittest.mock import MagicMock, patch, call

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from validators import UserValidator, InventoryValidator
from pricing import PriceCalculator, PercentDiscount, NoDiscount, get_discount_strategy
from inventory import InventoryManager
from repository import InMemoryOrderRepository
from notifier import EmailNotifier
from order_manager import OrderManager



@pytest.fixture
def users():
    return {
        "user1": {"email": "user1@example.com", "banned": False},
        "banned_user": {"email": "banned@example.com", "banned": True},
    }


@pytest.fixture
def inventory():
    return {
        "item1": {"price": 100.0, "stock": 10},
        "item2": {"price": 50.0, "stock": 5},
    }


@pytest.fixture
def price_calculator():
    return PriceCalculator(tax_rate=0.1)  # 10% налог


@pytest.fixture
def repository():
    return InMemoryOrderRepository()


@pytest.fixture
def mock_notifier():
    return MagicMock()


@pytest.fixture
def order_manager(users, inventory, price_calculator, repository, mock_notifier):
    return OrderManager(
        users=users,
        inventory=inventory,
        price_calculator=price_calculator,
        order_repository=repository,
        notifier=mock_notifier,
    )



class TestUserValidator:
    def test_valid_user_passes(self, users):
        v = UserValidator(users)
        v.validate("user1") 

    def test_unknown_user_raises(self, users):
        v = UserValidator(users)
        with pytest.raises(ValueError, match="не найден"):
            v.validate("ghost")

    def test_banned_user_raises(self, users):
        v = UserValidator(users)
        with pytest.raises(PermissionError, match="заблокирован"):
            v.validate("banned_user")



class TestInventoryValidator:
    def test_valid_items_pass(self, inventory):
        v = InventoryValidator(inventory)
        v.validate({"item1": 2})

    def test_unknown_item_raises(self, inventory):
        v = InventoryValidator(inventory)
        with pytest.raises(ValueError, match="не найден"):
            v.validate({"ghost_item": 1})

    def test_insufficient_stock_raises(self, inventory):
        v = InventoryValidator(inventory)
        with pytest.raises(ValueError, match="Недостаточно"):
            v.validate({"item1": 999})



class TestDiscountStrategies:
    def test_no_discount(self):
        assert NoDiscount().apply(100) == 100

    def test_percent_discount_10(self):
        assert PercentDiscount(10).apply(100) == pytest.approx(90.0)

    def test_percent_discount_20(self):
        assert PercentDiscount(20).apply(200) == pytest.approx(160.0)

    def test_get_strategy_none(self):
        assert isinstance(get_discount_strategy(None), NoDiscount)

    def test_get_strategy_save10(self):
        s = get_discount_strategy("SAVE10")
        assert s.apply(100) == pytest.approx(90.0)

    def test_get_strategy_save20(self):
        s = get_discount_strategy("SAVE20")
        assert s.apply(100) == pytest.approx(80.0)

    def test_unknown_promo_code_gives_no_discount(self):
        assert isinstance(get_discount_strategy("INVALID"), NoDiscount)



class TestPriceCalculator:
    def test_basic_price_with_tax(self, inventory):
        calc = PriceCalculator(tax_rate=0.1)
        total = calc.calculate({"item1": 2}, inventory, NoDiscount())
        assert total == pytest.approx(220.0)

    def test_price_with_discount_and_tax(self, inventory):
        calc = PriceCalculator(tax_rate=0.1)
        total = calc.calculate({"item1": 1}, inventory, PercentDiscount(10))
        assert total == pytest.approx(99.0)

    def test_multiple_items(self, inventory):
        calc = PriceCalculator(tax_rate=0.0)
        total = calc.calculate({"item1": 1, "item2": 2}, inventory, NoDiscount())
        assert total == pytest.approx(200.0)



class TestInventoryManager:
    def test_reserve_decreases_stock(self, inventory):
        mgr = InventoryManager(inventory)
        mgr.reserve({"item1": 3})
        assert inventory["item1"]["stock"] == 7

    def test_reserve_multiple_items(self, inventory):
        mgr = InventoryManager(inventory)
        mgr.reserve({"item1": 1, "item2": 2})
        assert inventory["item1"]["stock"] == 9
        assert inventory["item2"]["stock"] == 3



class TestInMemoryOrderRepository:
    def test_save_assigns_id(self):
        repo = InMemoryOrderRepository()
        order = repo.save({"user": "u1", "total": 100})
        assert order["id"] == 1

    def test_sequential_ids(self):
        repo = InMemoryOrderRepository()
        o1 = repo.save({"total": 10})
        o2 = repo.save({"total": 20})
        assert o1["id"] == 1
        assert o2["id"] == 2



class TestOrderManager:
    def test_successful_order_creation(self, order_manager, inventory, mock_notifier):
        order = order_manager.create_order("user1", {"item1": 2})
        assert order["id"] == 1
        assert order["status"] == "new"
        assert order["total"] == pytest.approx(220.0)
        assert inventory["item1"]["stock"] == 8

    def test_notifier_called_on_success(self, order_manager, mock_notifier):
        order = order_manager.create_order("user1", {"item1": 1})
        mock_notifier.send_order_confirmation.assert_called_once()
        call_args = mock_notifier.send_order_confirmation.call_args
        assert call_args[0][0] == "user1@example.com"

    def test_promo_code_applied(self, order_manager):
        order = order_manager.create_order("user1", {"item1": 1}, promo_code="SAVE10")
        assert order["total"] == pytest.approx(99.0)

    def test_unknown_user_raises(self, order_manager):
        with pytest.raises(ValueError):
            order_manager.create_order("nobody", {"item1": 1})

    def test_banned_user_raises(self, order_manager):
        with pytest.raises(PermissionError):
            order_manager.create_order("banned_user", {"item1": 1})

    def test_out_of_stock_raises(self, order_manager):
        with pytest.raises(ValueError):
            order_manager.create_order("user1", {"item1": 999})

    def test_notifier_not_called_on_failure(self, order_manager, mock_notifier):
        with pytest.raises(ValueError):
            order_manager.create_order("user1", {"item1": 999})
        mock_notifier.send_order_confirmation.assert_not_called()

    def test_email_notifier_uses_smtp(self, users, inventory, price_calculator, repository):
        """Тест EmailNotifier с mock SMTP."""
        with patch("notifier.smtplib.SMTP") as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server

            notifier = EmailNotifier("smtp.test.com", 587)
            manager = OrderManager(
                users=users,
                inventory=inventory,
                price_calculator=price_calculator,
                order_repository=repository,
                notifier=notifier,
            )
            manager.create_order("user1", {"item1": 1})

            mock_smtp_class.assert_called_once_with("smtp.test.com", 587)
            mock_server.sendmail.assert_called_once()
            mock_server.quit.assert_called_once()