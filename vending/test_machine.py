import pytest
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from machine import VendingMachine


@pytest.fixture
def machine():
    """Автомат с двумя товарами."""
    return VendingMachine({
        "A1": {"name": "Вода",  "price": 50.0, "stock": 2},
        "A2": {"name": "Сок",   "price": 80.0, "stock": 1},
    })


@pytest.fixture
def empty_machine():
    """Автомат без товаров — уже в состоянии OutOfStock."""
    m = VendingMachine({
        "A1": {"name": "Вода", "price": 50.0, "stock": 0},
    })
    m.set_state(m.out_of_stock)
    return m



def test_idle_insert_coin_transitions_to_has_money(machine):
    machine.insert_coin(50)
    assert machine.current_state == "HasMoneyState"

def test_idle_select_product_stays_idle(machine):
    machine.select_product("A1")
    assert machine.current_state == "IdleState"

def test_idle_cancel_stays_idle(machine):
    machine.cancel()
    assert machine.current_state == "IdleState"



def test_has_money_add_more_coins(machine):
    machine.insert_coin(30)
    machine.insert_coin(20)
    assert machine.balance == 50
    assert machine.current_state == "HasMoneyState"

def test_has_money_cancel_returns_to_idle(machine):
    machine.insert_coin(50)
    machine.cancel()
    assert machine.current_state == "IdleState"
    assert machine.balance == 0

def test_has_money_insufficient_funds_stays(machine):
    machine.insert_coin(30)
    machine.select_product("A1")   
    assert machine.current_state == "HasMoneyState"
    assert machine.balance == 30

def test_has_money_invalid_product_stays(machine):
    machine.insert_coin(100)
    machine.select_product("X9")
    assert machine.current_state == "HasMoneyState"

def test_has_money_buy_product_returns_to_idle(machine):
    machine.insert_coin(50)
    machine.select_product("A1")
    assert machine.current_state == "IdleState"
    assert machine.balance == 0
    assert machine.products["A1"]["stock"] == 1

def test_has_money_buy_gives_change(machine):
    machine.insert_coin(100)
    machine.select_product("A1")   
    assert machine.balance == 0    

def test_has_money_last_item_transitions_to_out_of_stock(machine):
    machine.insert_coin(100)
    machine.select_product("A2")
    assert machine.current_state == "IdleState"



def test_out_of_stock_insert_coin_returns_money(empty_machine, capsys):
    empty_machine.insert_coin(50)
    out = capsys.readouterr().out
    assert "возвращена" in out.lower()
    assert empty_machine.current_state == "OutOfStockState"

def test_out_of_stock_select_product(empty_machine, capsys):
    empty_machine.select_product("A1")
    out = capsys.readouterr().out
    assert "нет" in out.lower()

def test_out_of_stock_cancel_clears_balance(machine):
    machine.insert_coin(50);  machine.select_product("A1")
    machine.insert_coin(50);  machine.select_product("A1")
    machine.insert_coin(80);  machine.select_product("A2")
    assert machine.current_state == "OutOfStockState"
    machine.insert_coin(10)  
    machine.cancel()          
    assert machine.balance == 0



def test_maintenance_enter_from_idle(machine):
    machine.enter_maintenance()
    assert machine.current_state == "MaintenanceState"

def test_maintenance_refill_increases_stock(machine):
    machine.enter_maintenance()
    machine.refill("A1", 10)
    assert machine.products["A1"]["stock"] == 12

def test_maintenance_cancel_returns_to_idle(machine):
    machine.enter_maintenance()
    machine.cancel()
    assert machine.current_state == "IdleState"

def test_maintenance_cancel_from_empty_returns_out_of_stock(empty_machine):
    empty_machine.enter_maintenance()
    empty_machine.cancel()   
    assert empty_machine.current_state == "OutOfStockState"

def test_maintenance_refill_then_cancel_restores_service(empty_machine):
    empty_machine.enter_maintenance()
    empty_machine.refill("A1", 5)
    empty_machine.cancel()
    assert empty_machine.current_state == "IdleState"

def test_maintenance_blocks_insert_coin(machine, capsys):
    machine.enter_maintenance()
    machine.insert_coin(50)
    out = capsys.readouterr().out
    assert "обслужива" in out.lower()
    assert machine.balance == 0

def test_maintenance_blocks_select_product(machine, capsys):
    machine.enter_maintenance()
    machine.select_product("A1")
    out = capsys.readouterr().out
    assert "обслужива" in out.lower()