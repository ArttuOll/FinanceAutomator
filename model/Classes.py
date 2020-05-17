import datetime
import json
import os
from decimal import Decimal
from os import listdir
from os.path import isfile, join

import openpyxl
import pymysql
from openpyxl.styles import Font
from pymysql import DatabaseError


def clean_fragments(fragments_unclean):
    fragments = []
    for fragment in fragments_unclean:
        fragment = fragment.strip("\"")

        # Korvataan pilkut pisteillä
        if "," in fragment:
            fragment = fragment.replace(",", ".")

        fragments.append(fragment)

    return fragments


def get_filename_from_path(path):
    while True:
        file = [f for f in listdir(path) if isfile(join(path, f))]
        if len(file) != 1:
            print("Your transactions directory contains multiple files. It should only contain the latest one!")
            continue
        else:
            return file[0]


class JsonManager:

    def __init__(self):
        self.resources_dir = "resources"
        self.tag_file_name = "tags.json"
        self.self_dir = os.path.dirname(__file__)
        self.relative_path = os.path.join(self.resources_dir, self.tag_file_name)
        self.tag_file_path = os.path.join(self.self_dir, self.relative_path)

    def read_tags(self):
        with open(self.tag_file_path, "r") as tags_file:
            data = tags_file.read()
            categories_tags_object = json.loads(data)

        return categories_tags_object

    def write_tags(self, dictionary):
        with open(self.tag_file_name, "w", encoding="UTF-8") as categories_tags_file:
            json.dump(dictionary, categories_tags_file, ensure_ascii=False, indent=4)

        os.rename(self.tag_file_name, os.path.join(self.self_dir, self.relative_path))


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

    def __init__(self):
        self.events = []
        self.categories_tags_dict = None
        self.incomes, self.expenses = self.__sort_events(self.events)

    @staticmethod
    def __sort_events(events):
        negative_events = []
        positive_events = []
        for event in events:
            if event.amount < 0:
                negative_events.append(event)
            else:
                positive_events.append(event)
        return positive_events, negative_events

    @staticmethod
    def __count_sum_of_events(events):
        total = 0
        for event in events:
            total += event.amount
        return total

    def __get_balance(self):
        return self.__count_sum_of_events(self.incomes) + self.__count_sum_of_events(self.expenses)

    def __count_expenses_by_category(self):
        categories_values = {}
        for expense in self.expenses:
            name = expense.name.lower()
            for category in self.categories_tags_dict:
                total = 0
                for tag in category:
                    if tag in name:
                        total += Decimal(expense.amount)
                categories_values[category] = total

        return categories_values

    def __count_income_by_category(self):
        categories_values = {}
        for income_event in self.incomes:
            name = income_event.name.lower()
            for category in self.categories_tags_dict:
                total = 0
                for tag in category:
                    if tag in name:
                        total += Decimal(income_event.amount)
                categories_values[category] = total

        return categories_values

    def __create_event(self, fragments):
        if fragments[2] == "KORTTIOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            location = fragments[3]
            card_event = Event.card_payment(date=date, name=name, amount=amount, location=location)

            self.events.append(card_event)
            return

        elif fragments[2] == "PALKKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            salary_label = fragments[3]
            salary_event = Event.salary(date=date, name=name, amount=amount, salary_label=salary_label)

            self.events.append(salary_event)
            return

        elif fragments[2] == "AUTOM. NOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            cardnumber = fragments[3]
            atm_event = Event.atm_withdrawal(date=date, name=name, amount=amount, cardnumber=cardnumber)

            self.events.append(atm_event)
            return

        elif fragments[2] == "TILISIIRTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            refnumber = fragments[3]
            transfer_event = Event.bank_transfer(date=date, name=name, amount=amount, refnumber=refnumber)

            self.events.append(transfer_event)
            return

        elif fragments[2] == "VERKKOPANKKI":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            message = fragments[3]
            online_event = Event.online_bank(date=date, name=name, amount=amount, message=message)

            self.events.append(online_event)
            return

        elif fragments[2] == "SEPA PIKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            payment_number = fragments[3]
            mobile_event = Event.mobilepay(date=date, name=name, amount=amount, payment_number=payment_number)

            self.events.append(mobile_event)
            return

    def calculate_values_by_category(self):
        income_by_category = self.__count_income_by_category()

        # Lasketaan kokonaistulot ja muut tulot
        total_income = self.__count_sum_of_events(self.incomes)
        income_by_category["Total income"] = total_income

        other_income = total_income
        for category in income_by_category:
            other_income -= income_by_category[category]

        income_by_category["Other income"] = other_income

        # Lasketaan kokonaismenot ja muut menot
        expenses_by_category = self.__count_expenses_by_category()

        total_expenses = self.__count_sum_of_events(self.expenses)
        expenses_by_category["Total expenses"] = total_expenses

        other_expenses = total_expenses
        for category in expenses_by_category:
            other_expenses -= expenses_by_category[category]

        income_by_category["Other expenses"] = other_income

        # Yhdistetään molemmat sanakirjat yhdeksi, ottaen myös taseen mukaan
        values = {**income_by_category, **expenses_by_category, "Balance": self.__get_balance()}

        # Järjestetään sanakirja arvojen mukaan
        return {k: v for k, v in sorted(values.items(), key=lambda item: item[1])}

    def __extract_events_from_file(self, path):
        try:
            file = get_filename_from_path(path)
            path = os.path.join(path, file)
            with open(path, "r", encoding="iso-8859-1") as transactions_file:
                all_lines = transactions_file.read().splitlines()

                # Delete header row
                lines = all_lines[1:]

                for line in lines:
                    frags_unclean = line.split(";")

                    frags = clean_fragments(frags_unclean)
                    self.__create_event(frags)

        except FileNotFoundError:
            print("No such file!")
            return


class XlsxManager:

    def __init__(self):
        os.chdir("/home/bsuuv/Asiakirjat/talousseuranta")
        self.past_month = datetime.datetime.today().month - 1

    @staticmethod
    def __write_months_in_sheet(sheet):
        months = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu",
                  "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]

        for i in range(len(months)):
            month_column = chr(ord("B") + i)
            sheet[month_column + str(5)] = months[i]

    def init_workbooks(self):
        new_workbook = openpyxl.Workbook()
        sheet = new_workbook.active
        sheet.title = "taloushistoria"

        sheet["B1"] = "Taloushistoria"
        title_font = Font(size=16, bold=True)
        sheet["B1"].font = title_font

        self.__write_months_in_sheet(sheet)

        # Ensimmäisellä ajokerralla luodaan toissakuukauden tiedosto, jotta write_month() voi toimia
        # normaalisti
        new_workbook.save("talousseuranta_autom" + str(self.past_month - 1) + ".xlsx")

    def __write_values_in_sheet(self, sheet, values: list):
        month_column = chr(ord("A") + self.past_month)

        for i in range(len(values)):
            sheet[month_column + str(i + 6)] = values[i]

    def write_month(self, categories_values: dict):
        try:
            # Avataan kahden kuukauden takainen tiedosto muokattavaksi
            workbook = openpyxl.load_workbook("talousseuranta_autom" + str(self.past_month - 1) + ".xlsx")
        except FileNotFoundError:
            # Jos tiedostoa ei ole, eli ohjelmaa suoritetaan ensimmäisen kerran,
            # luodaan uusi ja kutsutaan metodia uudelleen
            self.init_workbooks()
            self.write_month(categories_values)
            return

        sheet = workbook["taloushistoria"]

        self.__write_categories_in_sheet(sheet, list(categories_values.keys()))
        self.__write_values_in_sheet(sheet, list(categories_values.values()))

        # Tallennetaan tiedosto uudella nimellä, edellinen jää varmuuskopioksi
        workbook.save("talousseuranta_autom" + str(self.past_month) + ".xlsx")

        # Poistetaan vanha varmuuskopio. Ensimmäisella ajokerralla kolmen kuukauden takaista tiedostoa
        # ei löydy
        try:
            os.remove("talousseuranta_autom" + str(self.past_month - 2) + ".xlsx")
        except FileNotFoundError:
            pass

    @staticmethod
    def __write_categories_in_sheet(sheet, categories):
        for i in range(len(categories)):
            sheet["A" + str(i + 6)] = categories[i]


class Dao:

    def __init__(self, address, username, password, database):
        self.address = address
        self.username = username
        self.password = password
        self.database = database

    def write_settings(self, directory):
        connection = pymysql.connect(self.address, self.username, self.password, self.database)

        cursor = connection.cursor()
        try:
            # Poistetaan edelliset asetukset ennen uusien tallentamista.
            cursor.execute("DELETE FROM settings;")
            cursor.execute("INSERT INTO settings VALUES %s", directory)
            connection.commit()
        except DatabaseError as error:
            print(error.args)
            print("Mitään ei tallennettu")
            connection.rollback()

        connection.close()

    def read_settings(self):
        connection = pymysql.connect(self.address, self.username, self.password, self.database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings;")

        settings = cursor.fetchone()
        connection.close()

        return settings
