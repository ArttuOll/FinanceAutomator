from decimal import Decimal

import pytest

from model.Classes import EventCalculator, Event, clean_fragments

# Pilkut muutettu pisteiksi, kuten pääskriptissäkin ennen Event-olioiden luomista.
expense1 = Event.card_payment("20.4.2020", "LIDL TRE FINLAYSON", Decimal("-5.25"), "'TAMPERE FIN")
expense2 = Event.card_payment("21.5.2020", "K MARKET", Decimal("-30.00"), "'KUOPIO FIN")
expense3 = Event.card_payment("21.5.2020", "salainen maksu", Decimal("-10.00"), "'KUOPIO FIN")
income1 = Event.salary("19.3.2020", "OSUMA", Decimal("100.25"), "10 PALKKA")
income2 = Event.salary("20.3.2020", "OSUMA", Decimal("15.50"), "10 PALKKA")
income3 = Event.salary("20.3.2020", "mystinen", Decimal("10.0"), "velat")
events = [expense1, expense2, expense3, income1, income2, income3]
categories_tags_dict = {
    "groceries": ["market", "lidl"],
    "salary": ["osuma"]
}


@pytest.fixture()
def handler():
    """Returns an EventHandler instanciated with specified events list."""
    return EventCalculator(events, categories_tags_dict)


def test_sort_expenses(handler):
    expenses = handler.expenses
    expected = [expense1, expense2, expense3]
    assert expenses == expected


def test_sort_incomes(handler):
    incomes = handler.incomes
    expected = [income1, income2, income3]
    assert incomes == expected


def test_calculate_values_by_category(handler):
    actual = handler.calculate_values_by_category()
    expected = {
        "Balance": Decimal("80.50"),
        "Other expenses": Decimal("-10.00"),
        "Other income": Decimal("10.00"),
        "Total income": Decimal("125.75"),
        "Total expenses": Decimal("-45.25"),
        "groceries": Decimal("-35.25"),
        "salary": Decimal("115.75")
    }
    assert actual == expected


def test_clean_fragment():
    test_string = """31.3.2020";"S MARKET KUOPIO";"KORTTIOSTO";"'KUOPIO FIN";"-26,21"""
    test_fragments = test_string.split(";")

    expected = ["31.3.2020", "S MARKET KUOPIO", "KORTTIOSTO", "KUOPIO FIN", "-26.21"]
    actual = clean_fragments(test_fragments)

    assert actual == expected
