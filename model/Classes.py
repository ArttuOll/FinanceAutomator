import datetime
import json
import os
from decimal import Decimal

import openpyxl


class Event:

    def __init__(self, date: str, name: str, amount: str, event_type=None, location=None, refnumber=None,
                 cardnumber=None,
                 message=None, salary_label=None, payment_number=None, category=None):
        self.date = date
        self.name = name
        self.amount = Decimal(amount)
        self.event_type = event_type
        self.location = location
        self.refnumber = refnumber
        self.cardnumber = cardnumber
        self.message = message
        self.salary_label = salary_label
        self.payment_number = payment_number

    @classmethod
    def bank_transfer(cls, date, name, amount, refnumber):
        date = date
        name = name
        amount = amount
        event_type = "TILISIIRTO"
        refnumber = refnumber
        return cls(date=date, name=name, amount=amount, event_type=event_type, refnumber=refnumber)

    @classmethod
    def card_payment(cls, date, name, amount, location):
        date = date
        name = name
        amount = amount
        event_type = "KORTTIOSTO"
        location = location
        return cls(date=date, name=name, amount=amount, event_type=event_type, location=location)

    @classmethod
    def atm_withdrawal(cls, date, name, amount, cardnumber):
        date = date
        name = name
        amount = amount
        event_type = "AUTOM. NOSTO"
        cardnumber = cardnumber
        return cls(date=date, name=name, amount=amount, event_type=event_type, cardnumber=cardnumber)

    @classmethod
    def online_bank(cls, date, name, amount, message):
        date = date
        name = name
        amount = amount
        event_type = "VERKKOPANKKI"
        message = message
        return cls(date=date, name=name, amount=amount, event_type=event_type, message=message)

    @classmethod
    def salary(cls, date, name, amount, salary_label):
        date = date
        name = name
        amount = amount
        event_type = "PALKKA"
        salary_label = salary_label
        return cls(date=date, name=name, amount=amount, event_type=event_type, salary_label=salary_label)

    @classmethod
    def mobilepay(cls, date, name, amount, payment_number):
        date = date
        name = name
        amount = amount
        event_type = "PALKKA"
        payment_number = payment_number
        return cls(date=date, name=name, amount=amount, event_type=event_type, payment_number=payment_number)


class EventHandler:

    def __init__(self, events):
        self.events = events
        self.tags = self.__read_tags()
        self.incomes, self.expenses = self.__sort_events()

    def __sort_events(self):
        negative_events = []
        positive_events = []
        for event in self.events:
            if event.amount < 0:
                negative_events.append(event)
            else:
                positive_events.append(event)
        return positive_events, negative_events

    def get_total(self, events):
        total = 0
        for event in events:
            total += event.amount
        return total

    def get_balance(self):
        return self.get_total(self.incomes) + self.get_total(self.expenses)

    def count_expenses_by_tag(self, tag):
        total = 0
        for expense in self.expenses:
            name = expense.name.lower()
            for keyword in self.tags[tag]:
                if keyword in name:
                    total += Decimal(expense.amount)

        return total

    def count_income_by_tag(self, tag):
        total = 0
        for income in self.incomes:
            name = income.name.lower()
            for keyword in self.tags[tag]:
                if keyword in name:
                    total += Decimal(income.amount)

        return total

    def __read_tags(self):
        script_dir = os.path.dirname(__file__)
        relative_dir = "resources/tags"
        absolute_dir = os.path.join(script_dir, relative_dir)
        with open(absolute_dir, "r") as tags_file:
            data = tags_file.read()
            tags_object = json.loads(data)

        return tags_object


class XlsxManager:

    def __init__(self):
        os.chdir("/home/bsuuv/Asiakirjat/talousseuranta")
        self.past_month = datetime.datetime.today().month - 1
        self.workbook = openpyxl.load_workbook("talousseuranta_autom" + str(self.past_month - 1) + ".xlsx")

    def init_new_workbook(self):
        # Tallennetaan muutettu taulukko.
        self.workbook.save("talousseuranta_autom" + str(self.past_month) + ".xlsx")

        # Poistetaan kahden kuukauden takainen taulukko.
        os.remove("talousseuranta_autom" + str(self.past_month - 1) + ".xlsx")

    def write_month(self, values):
        sheet = self.workbook["taloushistoria"]
        month_column = chr(ord("A") + self.past_month)

        # Oletetaan, että arvot ovat taulukon mukaisessa järjestyksessä.
        for i in range(6, 10):
            sheet[month_column + str(i)] = values[i - 6]
        for i in range(12, 17):
            sheet[month_column + str(i)] = values[i - 8]

        sheet[month_column + str(18)] = values[9]

        self.workbook.save("talousseuranta_autom.xlsx")



