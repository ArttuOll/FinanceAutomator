"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3
import os

from .model.dao import Dao
from .model.event_calculator import EventCalculator
from .model.event_extractor import EventExtractor
from .model.tag_manager import TagManager
from .model.xlsx_writer import XlsxWriter


def get_settings():
    """Ohjaa käyttää asettamaan ohjelman asetukset ja tallentaa ne."""

    dao = Dao("localhost", "root", "mariaonihana", "fa")
    save_dir, transactions_dir = dao.read_settings()

    if save_dir is None and transactions_dir is None:
        print("Asetukset on asetettava ennen laskemisen aloittamista.")
        save_dir, transactions_dir = choose_saving_and_transactions_dir()
        dao.write_settings(save_dir, transactions_dir)
        return save_dir, transactions_dir

    edited_save_dir, edited_transactions_dir = edit_directories_dialog()
    if edited_save_dir is not None and edited_transactions_dir is not None:
        save_dir = edited_save_dir
        transactions_dir = edited_transactions_dir

    return save_dir, transactions_dir


def get_categories_tags():
    """Lukee käyttäjän aiemmin asettamat kategoriat ja niiden tunnisteet
    tunnistetiedostosta. Jos tunnistetiedosto on tyhjä, käyttäjää pyydetään
    asettamaan ne. Jos tunnistetiedosto ei ollut tyhjä, käyttäjältä kysytään,
    haluaako hän muuttaa niitä."""

    tag_manager = TagManager()
    categories_tags_dict = tag_manager.read_tags()

    if categories_tags_dict == {}:
        print("Laskemisen kategorioita ei ole määritelty.")
        return set_categories_and_tags(tag_manager)

    edited_categories_tags = edit_categories_tags_dialog(tag_manager)
    if edited_categories_tags is not None:
        categories_tags_dict = edited_categories_tags

    return categories_tags_dict


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


def edit_directories_dialog():
    """Näyttää ohjelman vaatimien hakemistojen muuttamisdialogin ja asettaa ne
    uudelleen käyttäjän syötteen perusteelle"""

    print(("Haluatko muuttaa laskentataulukoiden tai tilitapahtumien"
        "sijainteja? (K, jos kyllä)?"))
    edit_directories = input()
    if edit_directories == "K":
        return choose_saving_and_transactions_dir()

    return None, None


def choose_saving_and_transactions_dir():
    """Opastaa käyttäjää asettamaan ohjelman asetuksiin hakemiston, johon
    ohjelman tuottamat laskentataulukot tallennetaan sekä hakemiston, josta
    laskemiseen käytettävät tiliote löytyy."""

    save_path_guidance_text = ("Polku kansioon, johon haluat laskentataulukot "
                               "tallennettavan.")
    edited_save_dir = get_and_validate_path(save_path_guidance_text)

    transactions_dir_guidance_text = "Polku kansioon, joka sisältää tiliotteen."
    edited_transactions_dir = get_and_validate_path(transactions_dir_guidance_text)

    return edited_save_dir, edited_transactions_dir


def edit_categories_tags_dialog(tag_manager):
    """Opastaa käyttäjää asettamaan tilitapahtumien luokitteluun käytettävät
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet. """
    print(("Haluatko muokata kategorioita ja niiden tunnisteita (K, jos "
        "kyllä)?"))
    edit_categories_tags = input()

    if edit_categories_tags == "K":
        return set_categories_and_tags(tag_manager)

    return None


def set_categories_and_tags(tag_manager):
    """Kirjoittaa tilitapahtumien tarkastelussa käytettävät
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet."""

    categories = read_categories()

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan
    # kuuluvat tunnisteet.
    tags = read_tags_for_categories(categories)

    categories_tags_dict = lists_to_dict(categories, tags)
    tag_manager.write_tags(categories_tags_dict)

    return categories_tags_dict


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


xlsx_dir, events_dir = get_settings()
categories_tags = get_categories_tags()

# Alustetaan EventCalculator käyttäjän asetusten pohjalta.
eventext = EventExtractor()
events = eventext.events_from_file(events_dir)
eventcalc = EventCalculator(events, categories_tags)

# Lasketaan käyttäjän antamia kategorioita vastaavat arvot.
print("Lasketaan kuukauden tuloja ja menoja...")
values_by_category = eventcalc.calculate_values()

# Alustetaan XlsxManager kirjoittamaan tulokset käyttäjän määrittämään
# hakemistoon ja kirjoitetaan tulokset .xlsx-tiedostoon.
xlsxmanager = XlsxWriter(xlsx_dir)

print("Kirjoitetaan tulokset tiedostoon talousseuranta_autom.xlsx...")
xlsxmanager.write_month(values_by_category)
