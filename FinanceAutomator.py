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
        print("Polku kansioon, joka sisältää tiliotteen.")
        path = input()
        transactions_file_name = ""

        if not os.path.exists(path):
            print("Polkua ei olemassa.")
            continue
        elif os.path.isfile(path):
            print("Antamasi polku johti tiedostoon, mutta tarvitaan hakemistoon johtava polku.")
            continue
        else:
            file = [f for f in listdir(path) if isfile(join(path, f))]
            if len(file) != 1:
                print("Tiliotteen sisältävässä kansiossa oli useampi kuin yksi tiedosto."
                      " Vain yhtä odotettiin.")
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
        print("Asetukset on asetettava ennen laskemisen aloittamista.")
        set_transactions_dir()

    elif categories_tags_dict == {}:
        print("Laskemisen kategorioita ei ole määritelty.")
        set_categories_and_tags()

    else:
        print("Haluatko muokata aiempia asetuksiasi?")
        edit_settings = input()

        if edit_settings == "K":
            set_transactions_dir()
        else:
            transactions_dir = settings[0]

        print("Haluatko uudelleen asettaa aiemmat kategorioit ja niiden tunnisteet?")
        edit_cats_tags = input()

        if edit_cats_tags == "K":
            set_categories_and_tags()


def set_categories_and_tags():
    global jsonmanager
    global eventcalc
    global categories_tags_dict

    categories = []

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan kuuluvat tunnisteet.
    tags = []

    while True:
        print("Anna kategorian nimi. Saatuasi kategorioiden ja tunnisteiden syöttämisen valmiiksi, syötä OK")
        category_name = input()

        if category_name == "OK":
            break

        categories.append(category_name)

        tags_of_category = []
        while True:
            print("""Syötä tunnisteita, joita esiintyy niiden tilitapahtumien nimissä, jotka kuuluvat antamaasi 
            kategoriaan. Ollessasi valmis syöta OK""")
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

print("Lasketaan kuukauden tuloja ja menoja...")
values_by_category = eventcalc.calculate_values_by_category()

print("Kirjoitetaan tulokset tiedostoon talousseuranta_autom.xlsx...")

xlsxmanager = XlsxManager()
xlsxmanager.write_month(values_by_category)
