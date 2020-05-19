#!/home/bsuuv/Ohjelmistoprojektit/venv/bin python
import os
from os import listdir
from os.path import isfile, join

from model.Classes import XlsxManager, Dao, JsonManager, EventCalculator, EventExtractor


def lists_to_dict(categories, tags):
    dictionary = {}

    categories_tags = zip(categories, tags)

    for category, tags in categories_tags:
        dictionary[category] = tags

    return dictionary


def choose_dir():
    while True:
        print("Path to directory containing your bank accounts events:")
        path = input()
        transactions_file_name = ""

        if not os.path.exists(path):
            print("Path does not exist.")
            continue
        elif os.path.isfile(path):
            print("The path you gave was to a file, but a path to a directory is needed!")
            continue
        else:
            file = [f for f in listdir(path) if isfile(join(path, f))]
            if len(file) != 1:
                print("Your transactions directory contains multiple files. It should only contain one!")
                continue
            else:
                transactions_file_name = file[0]
                break

    return os.path.join(path, transactions_file_name)


def set_transactions_dir():
    global transactions_dir

    transactions_dir = choose_dir()
    database.write_settings(transactions_dir)


def check_settings():
    global transactions_dir
    global categories_tags_dict
    global jsonmanager

    settings = database.read_settings()
    categories_tags_dict = jsonmanager.read_tags()

    if settings is None:
        print("It seems we'll have to do some settings before we begin\n")
        set_transactions_dir()

    elif categories_tags_dict == {}:
        print("No categories have been defined.")
        set_categories_and_tags()

    else:
        print("Would you like to edit your settings?")
        edit_settings = input()

        if edit_settings == "Y":
            set_transactions_dir()
        else:
            transactions_dir = settings[0]

        print("Would you like edit your categories and tags? ")
        edit_cats_tags = input()

        if edit_cats_tags == "Y":
            set_categories_and_tags()


def set_categories_and_tags():
    global jsonmanager
    global eventcalc
    global categories_tags_dict

    categories = []

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan kuuluvat tunnisteet.
    tags = []

    while True:
        print("Input category name. Type OK to finish setting up categories and tags.")
        category_name = input()

        if category_name == "OK":
            break

        categories.append(category_name)

        tags_of_category = []
        while True:
            print("""Input tags, parts of the receiver/sender strings of the transaction that can be used to 
            identify, which category the transaction belongs to. To finish inputting tags, type OK.""")
            tag = input()

            if tag == "OK":
                break

            tags_of_category.append(tag)

        tags.append(tags_of_category)

    categories_tags_dict = lists_to_dict(categories, tags)
    jsonmanager.write_tags(categories_tags_dict)


database = Dao("localhost", "root", "mariaonihana", "fa")
jsonmanager = JsonManager()
eventext = EventExtractor()

transactions_dir = ""

categories_tags_dict = {}

check_settings()

eventcalc = EventCalculator(eventext.events_from_file(transactions_dir),
                            categories_tags_dict)

print("Calculating incomes and expenses of the month...")
values_by_category = eventcalc.calculate_values_by_category()

print("Writing results to talousseuranta_autom.xlsx...")

try:
    xlsxmanager = XlsxManager()
    xlsxmanager.write_month(values_by_category)
except FileNotFoundError as e:
    print(e.strerror, "\n\nFatal error")
