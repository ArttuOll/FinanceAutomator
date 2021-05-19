"""Määrittelee luokan EventCalculator ja sen käyttämät apufunktiot."""
from decimal import Decimal

def _sort_by_sign(events):
    negative_events = [event for event in events if event.amount < 0]
    positive_events = [event for event in events if event.amount > 0]
    return positive_events, negative_events


def _count_sum_of_events(events):
    total = 0
    for event in events:
        total += event.amount

    return total


def _count_uncategorised_expenses(values_by_category, total_expenses):
    other_expenses = total_expenses
    for category in values_by_category:
        value = values_by_category[category]
        if value < 0:
            other_expenses += abs(value)

    return other_expenses


def _count_uncategorised_income(values_by_category, total_income):
    other_income = total_income
    for category in values_by_category:
        value = values_by_category[category]
        if value >= 0:
            other_income -= values_by_category[category]

    return other_income


class EventCalculator:
    """Hoitaa tilitapahtumiin liittyvän laskennan."""

    def __init__(self, events, categories_tags_dict):
        self.events = events
        self.categories_tags_dict = categories_tags_dict
        self.incomes, self.expenses = _sort_by_sign(self.events)

    def __count_balance(self):
        """Laskee taseen kaikki tilitapahtumat sisältävän luokkamuuttujan
        events avulla."""

        return _count_sum_of_events(self.incomes) + _count_sum_of_events(self.expenses)

    def __count_events_by_category(self):
        """Laskee käyttäjän antamien tilitapahtumien kategorioiden arvot
        käyttäjän antamien tunnisteiden avulla."""

        categories_values = {}
        for category in self.categories_tags_dict:
            total = 0
            for event in self.events:
                name = event.name.lower()
                for tag in self.categories_tags_dict[category]:
                    if tag in name:
                        total += Decimal(event.amount)
            categories_values[category] = total

        return categories_values

    def __count_atm_events(self):
        """Laskee käteisnostotapahtumien summan oliomuuttujan expenses
        avulla."""

        total = 0
        for expense in self.expenses:
            if expense.event_type == "AUTOM. NOSTO":
                total += expense.amount
        return total

    def calculate_values_by_category(self, include_totals=True):
        """Laskee käyttäjän antamien sekä vakiotilitapahtumakategorioiden
        arvot ja palauttaa ne sanakirjana."""

        total_income = _count_sum_of_events(self.incomes)
        total_expenses = _count_sum_of_events(self.expenses)

        values_by_category = self.__count_events_by_category()
        values_by_category["Käteisnostot"] = self.__count_atm_events()
        values_by_category["Muut tulot"] = _count_uncategorised_income(values_by_category, total_income)
        values_by_category["Muut menot"] = _count_uncategorised_expenses(values_by_category, total_expenses)

        if include_totals:
            values_by_category["Tulot yht."] = total_income
            values_by_category["Menot yht."] = total_expenses
            values_by_category["Tase"] = self.__count_balance()

        return values_by_category
