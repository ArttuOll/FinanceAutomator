#!/home/bsuuv/Ohjelmistoprojektit/venv/bin python
import os
from os import listdir
from os.path import isfile, join

from model.Classes import XlsxManager, Dao, TagManager, EventCalculator, EventExtractor


def lists_to_dict(categories, tags):
    """Yhdistää kaksi listaa sanakirjaksi."""
    dictionary = {}

    categories_tags = zip(categories, tags)

    for category, tags in categories_tags:
        dictionary[category] = tags

    return dictionary


def choose_dir():
    """Opastaa käyttäjää asettamaan ohjelman asetuksiin kansion, jossa tämän tiliotteet sijaitsevat."""
    global transactions_dir

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

    transactions_dir = os.path.join(path, transactions_file_name)
    database.write_settings(transactions_dir)


def check_settings():
    """Ohjaa käyttää asettamaan ohjelman asetukset ja tallentaa ne."""
    global transactions_dir
    global categories_tags_dict
    global jsonmanager

    settings = database.read_settings()
    categories_tags_dict = jsonmanager.read_tags()

    if settings is None:
        print("Asetukset on asetettava ennen laskemisen aloittamista.")
        choose_dir()

    elif categories_tags_dict == {}:
        print("Laskemisen kategorioita ei ole määritelty.")
        set_categories_and_tags()

    else:
        print("Haluatko muokata aiempia asetuksiasi?")
        edit_settings = input()

        if edit_settings == "K":
            choose_dir()
        else:
            transactions_dir = settings[0]

        print("Haluatko uudelleen asettaa kategorioita ja niiden tunnisteet?")
        edit_cats_tags = input()

        if edit_cats_tags == "K":
            set_categories_and_tags()


def set_categories_and_tags():
    """Ohjaa käyttäjää asettamaan tilitapahtumien tarkastelussa käytettävät kategoriat ja
    niiden tunnistamiseen käytettävät tunnisteet."""
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
jsonmanager = TagManager()
eventext = EventExtractor()
xlsxmanager = XlsxManager()

transactions_dir = ""
categories_tags_dict = {}

check_settings()

# Alustetaan EventCalculator käyttäjän asetusten pohjalta.
eventcalc = EventCalculator(eventext.events_from_file(transactions_dir),
                            categories_tags_dict)

# Lasketaan käyttäjän antamia kategorioita vastaavat arvot.
print("Lasketaan kuukauden tuloja ja menoja...")
values_by_category = eventcalc.calculate_values()

# Kirjoitetaan tulokset .xlsx-tiedostoon.
print("Kirjoitetaan tulokset tiedostoon talousseuranta_autom.xlsx...")
xlsxmanager.write_month(values_by_category)
