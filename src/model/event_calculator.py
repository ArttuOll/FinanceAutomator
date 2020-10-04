"""Hoitaa tilitapahtumiin liittyvän laskennan."""
from decimal import Decimal

class EventCalculator:
    def __init__(self, events, categories_tags_dict):
        self.events = events
        self.categories_tags_dict = categories_tags_dict
        self.incomes, self.expenses = self.__sort_events(self.events)


    def __sort_events(self, events):
        """Lajittelee tilitapahtumat positiivisiin ja negatiivisiin."""
        negative_events = []
        positive_events = []
        for event in events:
            if event.amount < 0:
                negative_events.append(event)
            else:
                positive_events.append(event)
        return positive_events, negative_events

    def __count_sum_of_events(self, events):
        """Laskee listassa olevien tilitapahtumien arvojen summan."""
        total = 0
        for event in events:
            total += event.amount
        return total

    def __count_balance(self):
        """Laskee taseen kaikki tilitapahtumat sisältävän luokkamuuttujan 
        events avulla."""
        return self.__count_sum_of_events(self.incomes) + self.__count_sum_of_events(self.expenses)

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

    def __count_other_income(self, values_by_category):
        """Laskee kategorioihin liittymättömien tulojen summan."""
        other_income = values_by_category["Tulot yht."]
        for category in values_by_category:
            value = values_by_category[category]
            if self.__is_expense_category(value, category):
                other_income -= values_by_category[category]
                
        return other_income


    def __is_expense_category(self, value, category):
        return value >= 0 and category != "Tulot yht." and category != "Käteisnostot"
        

    def __count_other_expenses(self, values_by_category):
        """Laskee kategorioihin liittymättömien menojen summan."""
        other_expenses = values_by_category["Menot yht."]
        for category in values_by_category:
            if values_by_category[category] < 0 and category != "Menot yht.":
                other_expenses -= values_by_category[category]
        return other_expenses

    def calculate_values(self):
        """Laskee käyttäjän antamien sekä vakiotilitapahtumakategorioiden 
        arvot ja palauttaa ne sanakirjana."""

        values_by_category = self.__count_events_by_category()

        # Lasketaan käteisnostot
        values_by_category["Käteisnostot"] = self.__count_atm_events()

        # Lasketaan kokonaistulot
        values_by_category["Tulot yht."] = self.__count_sum_of_events(self.incomes)

        # Lasketaan muut tulot
        values_by_category["Muut tulot"] = self.__count_other_income(values_by_category)

        # Lasketaan kokonaiskulut
        values_by_category["Menot yht."] = self.__count_sum_of_events(self.expenses)

        # Lasketaan muut kulut
        values_by_category["Muut menot"] = self.__count_other_expenses(values_by_category)

        values_by_category["Tase"] = self.__count_balance()

        return values_by_category
