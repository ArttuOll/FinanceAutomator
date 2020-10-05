"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3
import os

from .model.tag_manager import TagManager
from .model.event_calculator import EventCalculator
from .model.event_extractor import EventExtractor
from .model.xlsx_writer import XlsxWriter
from .model.dao import Dao


def check_settings():
    """Ohjaa käyttää asettamaan ohjelman asetukset ja tallentaa ne."""

    global TRANSACTIONS_DIR
    global SAVE_DIR
    global CATEGORIES_TAGS_DICT
    global TAG_MANAGER

    settings = database.read_settings()
    CATEGORIES_TAGS_DICT = TAG_MANAGER.read_tags()

    if settings is None:
        print("Asetukset on asetettava ennen laskemisen aloittamista.")
        choose_saving_and_transactions_dir()
        database.write_settings(TRANSACTIONS_DIR, SAVE_DIR)

    elif CATEGORIES_TAGS_DICT == {}:
        print("Laskemisen kategorioita ei ole määritelty.")
        set_categories_and_tags()

    else:
        edit_previous_settings_dialog(settings)


def get_and_validate_path(path_guidance_text):
    """Lukee käyttäjän syötteestä tiedostopolun ja tarkastaa, että se on
    olemassa ja että se johtaa hakemistoon."""

    while True:
        print(path_guidance_text)
        path = input()

        if not os.path.exists(path):
            print("Polkua ei olemassa.")
            continue

        if os.path.isfile(path):
            print(("Antamasi polku johti tiedostoon, mutta tarvitaan "
                    "hakemistoon johtava polku."))
            continue

        return path


def edit_previous_settings_dialog(settings):
    """Kysyy käyttäjältä, haluaako tämä muuttaa ohjelman aiempia asetuksia. Jos
    kyllä, ohjaa käyttäjän tallennuskansioiden ja tunnisteiden muokkaamis
    dialogeihin"""

    print("Haluatko muokata aiempia asetuksiasi? (K, jos kyllä)")
    edit_settings = input()

    if edit_settings == "K":
        edit_directories_dialog(settings)
        edit_categories_tags_dialog()


def edit_directories_dialog(settings):
    """Näyttää ohjelman vaatimien hakemistojen muuttamisdialogin ja asettaa ne
    uudelleen käyttäjän syötteen perusteelle"""

    global TRANSACTIONS_DIR
    global SAVE_DIR

    print(("Haluatko muuttaa laskentataulukoiden tai tilitapahtumien"
        "sijainteja? (K, jos kyllä)?"))
    edit_directories = input()
    if edit_directories == "K":
        choose_saving_and_transactions_dir()
    else:
        TRANSACTIONS_DIR = settings[0]
        SAVE_DIR = settings[1]


def choose_saving_and_transactions_dir():
    """Opastaa käyttäjää asettamaan ohjelman asetuksiin hakemiston, johon
    ohjelman tuottamat laskentataulukot tallennetaan sekä hakemiston, josta
    laskemiseen käytettävät tiliote löytyy."""

    global SAVE_DIR
    global TRANSACTIONS_DIR

    save_path_guidance_text = ("Polku kansioon, johon haluat laskentataulukot "
                               "tallennettavan.")
    SAVE_DIR = get_and_validate_path(save_path_guidance_text)

    transactions_dir_guidance_text = "Polku kansioon, joka sisältää tiliotteen."
    TRANSACTIONS_DIR = get_and_validate_path(transactions_dir_guidance_text)


def edit_categories_tags_dialog():
    """Opastaa käyttäjää asettamaan tilitapahtumien luokitteluun käytettävät
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet. """
    print(("Haluatko muokata kategorioita ja niiden tunnisteita (K, jos "
        "kyllä)?"))
    edit_categories_tags = input()

    if edit_categories_tags == "K":
        set_categories_and_tags()


def set_categories_and_tags():
    """Kirjoittaa tilitapahtumien tarkastelussa käytettävät
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet."""

    global TAG_MANAGER
    global eventcalc
    global CATEGORIES_TAGS_DICT

    categories = read_categories()

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan
    # kuuluvat tunnisteet.
    tags = read_tags_for_categories(categories)

    CATEGORIES_TAGS_DICT = lists_to_dict(categories, tags)
    TAG_MANAGER.write_tags(CATEGORIES_TAGS_DICT)


def read_categories():
    """Lukee tilitapahtumien tarkastelussa käytettävät kategoriat käyttäjän
    syötteestä."""

    categories = []
    while True:
        print(("Anna kategorian nimi. Saatuasi kategorioiden ja tunnisteiden "
                "syöttämisen valmiiksi, syötä OK"))
        category_name = input()

        if category_name == "OK":
            break

        categories.append(category_name)

    return categories


def read_tags_for_categories(categories):
    """Lukee annettuja kategorioita vastaavat tunnisteet käyttäjän
    syötteestä"""

    tags = []
    for category in categories:
        tags_of_category = read_tags_for_category(category)
        tags.append(tags_of_category)

    return tags


def read_tags_for_category(category):
    """Lukee annettua kategoriaa vastaavat tunnisteet käyttäjän syötteestä"""

    tags_of_category = []
    while True:
        print(("Syötä tunnisteita, joita esiintyy niiden tilitapahtumien "
                f"nimissä, jotka kuuluvat kategoriaan {category}. Ollessasi "
                "valmis syöta OK"))
        tag = input()

        if tag == "OK":
            break

        tags_of_category.append(tag)

    return tags_of_category


def lists_to_dict(list1, list2):
    """Yhdistää kaksi listaa sanakirjaksi."""

    dictionary = {}

    tuples_zip = zip(list1, list2)

    for item1, item2 in tuples_zip:
        dictionary[item1] = item2

    return dictionary


database = Dao("localhost", "root", "mariaonihana", "fa")
TAG_MANAGER = TagManager()
eventext = EventExtractor()

SAVE_DIR = ""
TRANSACTIONS_DIR = ""
CATEGORIES_TAGS_DICT = {}

check_settings()

# Alustetaan EventCalculator käyttäjän asetusten pohjalta.
eventcalc = EventCalculator(eventext.events_from_file(TRANSACTIONS_DIR),
                            CATEGORIES_TAGS_DICT)

# Lasketaan käyttäjän antamia kategorioita vastaavat arvot.
print("Lasketaan kuukauden tuloja ja menoja...")
values_by_category = eventcalc.calculate_values()

# Alustetaan XlsxManager kirjoittamaan tulokset käyttäjän määrittämään
# hakemistoon ja kirjoitetaan tulokset .xlsx-tiedostoon.
xlsxmanager = XlsxWriter(SAVE_DIR)

print("Kirjoitetaan tulokset tiedostoon talousseuranta_autom.xlsx...")
xlsxmanager.write_month(values_by_category)
