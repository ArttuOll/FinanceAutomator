from decimal import Decimal

import pytest

from model.Classes import EventHandler, Event

# Pilkut muutettu pisteiksi, kuten pääskriptissäkin ennen Event-olioiden luomista.
expense1 = Event.card_payment("20.4.2020", "LIDL TRE FINLAYSON", Decimal(-5.25), "'TAMPERE FIN")
expense2 = Event.card_payment("21.5.2020", "K MARKET", Decimal(-30.00), "'KUOPIO FIN")
income1 = Event.salary("19.3.2020", "OSUMA", Decimal(100.25), "10 PALKKA")
income2 = Event.salary("20.3.2020", "OSUMA", Decimal(15.50), "10 PALKKA")
events = [expense1, expense2, income1, income2]


@pytest.fixture
def handler():
    """Returns an EventHandler instanciated with specified events list."""
    return EventHandler(events)


def test_sort_expenses(handler):
    expenses = handler.expenses
    expected = [expense1, expense2]
    assert expenses == expected


def test_sort_incomes(handler):
    incomes = handler.incomes
    expected = [income1, income2]
    assert incomes == expected


def test_addition_minusminus(handler):
    total_expenses = handler.__count_sum_of_events(handler.expenses)
    expected = -35.25
    assert total_expenses == expected


def test_addition_plusplus(handler):
    total_incomes = handler.__count_sum_of_events(handler.incomes)
    expected = 115.75
    assert total_incomes == expected


def test_addition_plusminus(handler):
    balance = handler.__get_balance()
    expected = Decimal(80.5)
    assert balance == expected


def test_calculate_by_tag(handler):
    salary = handler.__count_income_by_category("salary")
    expected = Decimal(115.75)
    assert salary == expected
