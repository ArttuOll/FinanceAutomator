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
        fragment = fragment.strip("\'")

        # Korvataan pilkut pisteillä
        if "," in fragment:
            fragment = fragment.replace(",", ".")

        fragments.append(fragment)

    return fragments


class TagManager:
    """Huolehtii tunnisteiden lukemisesta ja kirjoittamisesta tunnistetiedostoon."""

    def __init__(self):
        self.resources_dir = "resources"
        self.tag_file_name = "tags.json"
        self.self_dir = os.path.dirname(__file__)
        self.relative_path = os.path.join(self.resources_dir, self.tag_file_name)
        self.tag_file_path = os.path.join(self.self_dir, self.relative_path)

    def read_tags(self):
        """Lukee kategoriat ja niitä vastaavat tunnisteet tunnistetiedostosta ja palauttaa ne
        sanakirjana."""
        with open(self.tag_file_path, "r") as tags_file:
            data = tags_file.read()
            categories_tags_object = json.loads(data)

        return categories_tags_object

    def write_tags(self, dictionary):
        """Kirjoittaa kategoriat ja niitä vastaavat tunnisteet tunnistetiedostoon JSON-muodossa."""
        with open(self.tag_file_name, "w", encoding="UTF-8") as categories_tags_file:
            json.dump(dictionary, categories_tags_file, ensure_ascii=False, indent=4)

        os.rename(self.tag_file_name, os.path.join(self.self_dir, self.relative_path))


class Event:
    """Kuvaa yhtä tilitapahtumaa. Sisältää tilitapahtuman ominaisuudet. Muokattava vastaamaan
    käyttäjän pankin tarjoaman tilitapahtumatiedoston kenttiä."""

    def __init__(self, date: str, name: str, amount: str, event_type=None, location=None, refnumber=None,
                 cardnumber=None,
                 message=None, salary_label=None, payment_number=None):
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
        event_type = "SEPA PIKA"
        payment_number = payment_number
        return cls(date=date, name=name, amount=amount, event_type=event_type, payment_number=payment_number)


class EventCalculator:
    """Hoitaa kaiken tilitapahtumiin liittyvän laskennan."""

    def __init__(self, events, categories_tags_dict):
        self.events = events
        self.categories_tags_dict = categories_tags_dict
        self.incomes, self.expenses = self.__sort_events(self.events)

    @staticmethod
    def __sort_events(events):
        """Lajittelee tilitapahtumat positiivisiin ja negatiivisiin."""
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
        """Laskee listassa olevien tilitapahtumien arvojen summan."""
        total = 0
        for event in events:
            total += event.amount
        return total

    def __count_balance(self):
        """Laskee taseen kaikki tilitapahtumat sisältävän luokkamuuttujan events avulla."""
        return self.__count_sum_of_events(self.incomes) + self.__count_sum_of_events(self.expenses)

    def __count_events_by_category(self):
        """Laskee käyttäjän antamien tilitapahtumien kategorioiden arvot käyttäjän antamien tunnisteiden
         avulla."""
        categories_values = {}
        for category in self.categories_tags_dict:
            total = 0
            for expense in self.events:
                name = expense.name.lower()
                for tag in self.categories_tags_dict[category]:
                    if tag in name:
                        total += Decimal(expense.amount)
            categories_values[category] = total

        return categories_values

    def __count_atm_events(self):
        """Laskee käteisnostotapahtumien summan luokkamuuttujan expenses avulla."""
        total = 0
        for expense in self.expenses:
            if expense.event_type == "AUTOM. NOSTO":
                total += expense.amount
        return total

    @staticmethod
    def __count_other_income(values_by_category):
        """Laskee kategorioihin liittymättömien tulojen summan."""
        other_income = values_by_category["Tulot yht."]
        for category in values_by_category:
            if values_by_category[category] >= 0 and category != "Tulot yht." and category != "Käteisnostot":
                other_income -= values_by_category[category]
        return other_income

    @staticmethod
    def __count_other_expenses(values_by_category):
        """Laskee kategorioihin liittymättömien menojen summan."""
        other_expenses = values_by_category["Menot yht."]
        for category in values_by_category:
            if values_by_category[category] < 0 and category != "Menot yht.":
                other_expenses -= values_by_category[category]
        return other_expenses

    def calculate_values(self):
        """Laskee käyttäjän antamien sekä vakiotilitapahtumakategorioiden arvot ja palauttaa ne
        sanakirjana."""

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


class EventExtractor:
    """Lukee tilitapahtumat sisältävän tiedoston ja muuntaa sen Event-olioita sisältäväksi listaksi."""

    def events_from_file(self, path):
        """Hoitaa tilitapahtumat sisältävän tiedoston lukemisen ja Event-olioita sisältävän listan
        palauttamisen."""
        file = os.path.join(path, self.__read_only_filename_from_directory(path))
        try:
            events = []
            with open(file, "r", encoding="iso-8859-1") as transactions_file:
                all_lines = transactions_file.read().splitlines()

                # Delete header row
                lines = all_lines[1:]

                for line in lines:
                    frags_unclean = line.split(";")

                    frags = clean_fragments(frags_unclean)
                    events.append(self.__create_event(frags))

            return events

        except FileNotFoundError:
            print("Tiedostoa ei ole olemassa.")
            return

    @staticmethod
    def __create_event(fragments):
        """Luo ja palauttaa oikean tyyppisen Event-olion perustuen tilitapahtumatiedostossa määriteltyyn
        tapahtumatyyppiin."""
        if fragments[2] == "KORTTIOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            location = fragments[3]

            return Event.card_payment(date=date, name=name, amount=amount, location=location)

        elif fragments[2] == "PALKKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            salary_label = fragments[3]

            return Event.salary(date=date, name=name, amount=amount, salary_label=salary_label)

        elif fragments[2] == "AUTOM. NOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            cardnumber = fragments[3]

            return Event.atm_withdrawal(date=date, name=name, amount=amount, cardnumber=cardnumber)

        elif fragments[2] == "TILISIIRTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            refnumber = fragments[3]

            return Event.bank_transfer(date=date, name=name, amount=amount, refnumber=refnumber)

        elif fragments[2] == "VERKKOPANKKI":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            message = fragments[3]

            return Event.online_bank(date=date, name=name, amount=amount, message=message)

        elif fragments[2] == "SEPA PIKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            payment_number = fragments[3]

            return Event.mobilepay(date=date, name=name, amount=amount, payment_number=payment_number)

    @staticmethod
    def __read_only_filename_from_directory(path):
        file = [f for f in listdir(path) if isfile(join(path, f))]
        if len(file) != 1:
            print("Tiliotteen sisältävässä kansiossa oli useampi kuin yksi tiedosto."
                  " Vain yhtä odotettiin. Poista muut tiedostot ja aja ohjelma uudelleen.")
        else:
            return file[0]


class XlsxManager:
    """Hoitaa xlsx-tiedostoihin liittyvät toiminnot."""

    def __init__(self, save_dir):
        os.chdir(save_dir)
        # Ohjelmalle annetaan aina edellisen kuukauden tilitapahtumat.
        self.past_month = datetime.datetime.today().month - 1

    @staticmethod
    def __write_months_in_sheet(sheet):
        """Kirjoittaa kuukausien nimet xlsx-tiedostoon."""
        months = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu",
                  "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]

        for i in range(len(months)):
            month_column = chr(ord("B") + i)
            sheet[month_column + str(5)] = months[i]

    def init_workbooks(self):
        """Luo uuden xlsx-tiedoston ja alustaa uuden laskentataulukon."""
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
        """Kirjoittaa annetut arvot annettuun laskentataulukkoon oikeaa kuukautta vastaavaan sarakkeeseen."""
        month_column = chr(ord("A") + self.past_month)

        for i in range(len(values)):
            sheet[month_column + str(i + 6)] = values[i]

    def write_month(self, categories_values: dict):
        """Kirjoittaa laskentataulukkoon edellistä kuukautta vastaavat arvot."""
        try:
            # Avataan kahden kuukauden takainen tiedosto muokattavaksi
            workbook = openpyxl.load_workbook("talousseuranta_autom" + str(self.past_month - 1) + ".xlsx")
        except FileNotFoundError:
            # Jos tiedostoa ei ole, eli ohjelmaa suoritetaan ensimmäisen kerran,
            # luodaan uusi xlsx-tiedosto ja kutsutaan metodia uudelleen.
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
        """Kirjoittaa laskentataulukkoon käyttäjän antamat tilitapahtumakategoriat."""
        for i in range(len(categories)):
            sheet["A" + str(i + 6)] = categories[i]


class Dao:
    """Huolehtii tietokantaan kirjoittamisesta ja sieltä lukemisesta."""

    def __init__(self, address, username, password, database):
        self.address = address
        self.username = username
        self.password = password
        self.database = database

    def write_settings(self, transactions_dir, save_dir):
        """Kirjoittaa annetut asetukset tietokantaan. Tällä hetkellä ainoa asetus on tilitapahtumat
        sisältävän tiedoston sijainti (muuttuja directory)."""
        connection = pymysql.connect(self.address, self.username, self.password, self.database)

        cursor = connection.cursor()
        try:
            # Poistetaan edelliset asetukset ennen uusien tallentamista.
            cursor.execute("DELETE FROM settings;")
            cursor.execute("INSERT INTO settings VALUES (%s, %s)", (transactions_dir, save_dir))
            connection.commit()
        except DatabaseError as error:
            print(error.args)
            print("Nothing was saved")
            connection.rollback()

        connection.close()

    def read_settings(self):
        """Lukee asetukset tietokannasta ja palauttaa ne yhtenä muuttujana."""
        connection = pymysql.connect(self.address, self.username, self.password, self.database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings;")

        settings = cursor.fetchone()
        connection.close()

        return settings
