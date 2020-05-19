from decimal import Decimal

import pytest

from model.Classes import EventCalculator, Event

# Pilkut muutettu pisteiksi, kuten pääskriptissäkin ennen Event-olioiden luomista.
expense1 = Event.card_payment("20.4.2020", "LIDL TRE FINLAYSON", Decimal("-5.25"), "'TAMPERE FIN")
expense2 = Event.card_payment("21.5.2020", "K MARKET", Decimal("-30.00"), "'KUOPIO FIN")
income1 = Event.salary("19.3.2020", "OSUMA", Decimal("100.25"), "10 PALKKA")
income2 = Event.salary("20.3.2020", "OSUMA", Decimal("15.50"), "10 PALKKA")
events = [expense1, expense2, income1, income2]
categories_tags_dict = {
    "groceries": ["market", "lidl"],
    "salary": ["osuma"]
}


class TestCalculations:

    @pytest.fixture()
    def handler(self):
        """Returns an EventHandler instanciated with specified events list."""
        return EventCalculator(events, categories_tags_dict)

    def test_sort_expenses(self, handler):
        expenses = handler.expenses
        expected = [expense1, expense2]
        assert expenses == expected

    def test_sort_incomes(self, handler):
        incomes = handler.incomes
        expected = [income1, income2]
        assert incomes == expected

    def test_calculate_values_by_category(self, handler):
        actual = handler.calculate_values_by_category()
        expected = {
            "Balance": Decimal("80.50"),
            "Other expenses": Decimal("0"),
            "Other income": Decimal("0"),
            "Total income": Decimal("115.75"),
            "Total expenses": Decimal("-35.25"),
            "groceries": Decimal("-35.25"),
            "salary": Decimal("115.75")
        }
        assert actual == expected
