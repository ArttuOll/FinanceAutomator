"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3
import os

from models import XlsxManager, Dao, TagManager, EventCalculator, EventExtractor


def check_settings():
    """Ohjaa käyttää asettamaan ohjelman asetukset ja tallentaa ne."""
    global transactions_dir
    global save_dir
    global categories_tags_dict
    global jsonmanager

    settings = database.read_settings()
    categories_tags_dict = jsonmanager.read_tags()

    if settings is None:
        print("Asetukset on asetettava ennen laskemisen aloittamista.")
        choose_saving_and_transactions_dir()
        database.write_settings(transactions_dir, save_dir)

    elif categories_tags_dict == {}:
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
        elif os.path.isfile(path):
            print(("Antamasi polku johti tiedostoon, mutta tarvitaan "
                    "hakemistoon johtava polku."))
            continue
        else:
            return path


def edit_previous_settings_dialog(settings):
        print("Haluatko muokata aiempia asetuksiasi? (K, jos kyllä)")
        edit_settings = input()

        if edit_settings == "K":
            edit_directories_dialog(settings)
            edit_categories_tags_dialog()


def edit_directories_dialog(settings):
    print(("Haluatko muuttaa laskentataulukoiden tai tilitapahtumien"
        "sijainteja? (K, jos kyllä)?"))
    edit_directories = input()
    if edit_directories == "K":
        choose_saving_and_transactions_dir()
    else:
        transactions_dir = settings[0]
        save_dir = settings[1]


def choose_saving_and_transactions_dir():
    """Opastaa käyttäjää asettamaan ohjelman asetuksiin hakemiston, johon 
    ohjelman tuottamat laskentataulukot tallennetaan sekä hakemiston, josta 
    laskemiseen käytettävät tiliote löytyy."""
    global save_dir
    global transactions_dir

    save_path_guidance_text = ("Polku kansioon, johon haluat laskentataulukot "
                               "tallennettavan.")
    save_dir = get_and_validate_path(save_path_guidance_text)

    transactions_dir_guidance_text = "Polku kansioon, joka sisältää tiliotteen."
    transactions_dir = get_and_validate_path(transactions_dir_guidance_text)


def edit_categories_tags_dialog():
    print(("Haluatko muokata kategorioita ja niiden tunnisteita (K, jos "
        "kyllä)?"))
    edit_categories_tags = input()

    if edit_categories_tags == "K":
        set_categories_and_tags()


def set_categories_and_tags():
    """Ohjaa käyttäjää asettamaan tilitapahtumien tarkastelussa käytettävät 
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet."""
    global jsonmanager
    global eventcalc
    global categories_tags_dict

    categories = read_categories()

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan 
    # kuuluvat tunnisteet.
    tags = read_tags_for_categories(categories)

    categories_tags_dict = lists_to_dict(categories, tags)
    jsonmanager.write_tags(categories_tags_dict)


def read_categories():
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
    tags = []
    for category in categories:
        tags_of_category = read_tags_for_category(category)
        tags.append(tags_of_category)
    
    return tags


def read_tags_for_category(category):
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
jsonmanager = TagManager()
eventext = EventExtractor()

save_dir = ""
transactions_dir = ""
categories_tags_dict = {}

check_settings()

# Alustetaan EventCalculator käyttäjän asetusten pohjalta.
eventcalc = EventCalculator(eventext.events_from_file(transactions_dir),
                            categories_tags_dict)

# Lasketaan käyttäjän antamia kategorioita vastaavat arvot.
print("Lasketaan kuukauden tuloja ja menoja...")
values_by_category = eventcalc.calculate_values()

# Alustetaan XlsxManager kirjoittamaan tulokset käyttäjän määrittämään hakemistoon ja kirjoitetaan tulokset
# .xlsx-tiedostoon.
xlsxmanager = XlsxManager(save_dir)

print("Kirjoitetaan tulokset tiedostoon talousseuranta_autom.xlsx...")
xlsxmanager.write_month(values_by_category)
