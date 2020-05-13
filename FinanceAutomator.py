#!/home/bsuuv/Ohjelmistoprojektit/venv/bin python
import gettext
import os
from os import listdir
from os.path import join, isfile

from model.Classes import Event, EventHandler, XlsxManager, Dao, JsonManager

fi = gettext.translation("fi_FI", localedir="locale", languages=["fi"])
_ = fi.gettext


def clean_fragments(fragments_unclean):
    fragments = []
    for fragment in fragments_unclean:
        fragment = fragment.strip("\"")

        # Korvataan pilkut pisteillä
        if "," in fragment:
            fragment = fragment.replace(",", ".")

        fragments.append(fragment)

    return fragments


def create_event(fragments):
    if fragments[2] == "KORTTIOSTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        location = fragments[3]
        card_event = Event.card_payment(date=date, name=name, amount=amount, location=location)

        return card_event

    elif fragments[2] == "PALKKA":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        salary_label = fragments[3]
        salary_event = Event.salary(date=date, name=name, amount=amount, salary_label=salary_label)

        return salary_event

    elif fragments[2] == "AUTOM. NOSTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        cardnumber = fragments[3]
        atm_event = Event.atm_withdrawal(date=date, name=name, amount=amount, cardnumber=cardnumber)

        return atm_event

    elif fragments[2] == "TILISIIRTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        refnumber = fragments[3]
        transfer_evet = Event.bank_transfer(date=date, name=name, amount=amount, refnumber=refnumber)

        return transfer_evet

    elif fragments[2] == "VERKKOPANKKI":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        message = fragments[3]
        online_event = Event.online_bank(date=date, name=name, amount=amount, message=message)

        return online_event

    elif fragments[2] == "SEPA PIKA":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        payment_number = fragments[3]
        mobile_event = Event.mobilepay(date=date, name=name, amount=amount, payment_number=payment_number)

        return mobile_event


def calculate_values():
    global jsonManager
    handler = EventHandler(events, jsonManager.read_tags())

    total_income = handler.get_total(handler.incomes)
    salary = handler.count_income_by_tag("salary")
    benefits = handler.count_income_by_tag("benefit")
    other_income = total_income - salary - benefits

    total_expenses = handler.get_total(handler.expenses)
    groceries = handler.count_expenses_by_tag("grocery")
    electricity = handler.count_expenses_by_tag("electricity")
    rent = handler.count_expenses_by_tag("rent")
    internet = handler.count_expenses_by_tag("internet")
    other_expenses = total_expenses - groceries - rent - electricity - internet

    balance = handler.get_balance()

    values = [benefits, salary, other_income, total_income, groceries, electricity, rent, other_expenses,
              total_expenses, balance]
    return values


def get_filename_from_path(path):
    while True:
        file = [f for f in listdir(path) if isfile(join(path, f))]
        if len(file) != 1:
            print(_("Your transactions directory contains multiple files. It should only contain the latest one!"))
            continue
        else:
            return file[0]


def extract_events_from_file(path):
    events = []
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
                event = create_event(frags)
                events.append(event)

    except FileNotFoundError:
        print(_("No such file!"))
        return

    return events


def choose_language():
    while True:
        print("Choose language by typing FI for finnish or EN for english")
        lang = input()

        if lang == "EN" or lang == "FI":
            break
        else:
            print(_("Invalid language selection."))

    return lang


def choose_dir():
    while True:
        print(_("Path to directory containing your bank accounts events:"))
        path = input()

        if not os.path.exists(path):
            print(_("Path does not exist."))
            continue
        elif os.path.isfile(path):
            print(_("The path you gave was to a file, but a path to a directory is needed!"))
            continue
        else:
            break

    return path


def setup_settings():
    global language
    global transactions_dir

    settings = database.read_settings()
    if settings is None:
        print(_("It seems we'll have to do some settings before we begin\n"))
        choose_settings()
    else:
        print(_("Would you like to edit your settings? Type Y for yes or N for no."))
        edit_settings = input()

        if edit_settings == "Y":
            choose_settings()
            return
        else:
            language, transactions_dir = settings


def categories_and_tags_to_dict(categories, tags):
    dictionary = {}

    categories_tags = zip(categories, tags)

    for category, tags in categories_tags:
        dictionary[category] = tags

    return dictionary


def set_categories_and_tags():
    global jsonManager

    categories = []

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan kuuluvat tunnisteet.
    tags = []

    while True:
        print(_("Input category name. Type OK to finish setting up categories and tags."))
        category_name = input()

        if category_name == "OK":
            break

        categories.append(category_name)

        tags_of_category = []
        while True:
            print(_("""Input tags, parts of the receiver/sender strings of the transaction that can be used to 
            identify, which category the transaction belongs to. To finish inputting tags, type OK."""))
            tag = input()

            if tag == "OK":
                break

            tags_of_category.append(tag)

        tags.append(tags_of_category)

    dictionary = categories_and_tags_to_dict(categories, tags)

    jsonManager.write_tags(dictionary)


def choose_settings():
    global language
    global transactions_dir

    language = choose_language()
    transactions_dir = choose_dir()

    print(_("Would you like to reset your categories and tags? Y for yes or N for no"))
    reset = input()

    if reset == "Y":
        set_categories_and_tags()

    database.write_settings(language, transactions_dir)


database = Dao("localhost", "root", "mariaonihana", "fa")
jsonManager = JsonManager()
language = ""
transactions_dir = ""

setup_settings()

if language == "FI":
    fi.install()

events = extract_events_from_file(transactions_dir)

print(_("Calculating incomes and expenses of the month..."))
values = calculate_values()

print(_("Writing results to talousseuranta_autom.xlsx..."))

try:
    xlsxmanager = XlsxManager()
    xlsxmanager.write_month(values)
except FileNotFoundError as e:
    print(e.strerror, _("\n\nFatal error"))
