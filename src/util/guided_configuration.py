"""Ohjaa käyttäjää asettamaan ohjelman asetukset ja palauttaa ne sanakirjana"""
import os
from sys import stderr

from ..model.configs import Configs


def guided_configuration():
    """Ohjaa käyttää asettamaan ohjelman asetukset ja tallentaa ne."""

    print("""Ohjattu asetusten asettaminen

            Paina enter syötettyäsi arvon. Syötä tyhjä arvo säilyttääksesi
            vakioasetuksen.""")

    save_dir = choose_save_dir()
    categories_tags = read_categories_tags()

    configs = Configs()
    configs.set_config("save_dir", save_dir)
    configs.set_config("categories_tags", categories_tags)
    configs.write()


def choose_save_dir():
    """Opastaa käyttäjää asettamaan ohjelman asetuksiin hakemiston, johon
    ohjelman tuottamat laskentataulukot tallennetaan."""

    save_path_guidance_text = ("Polku kansioon, johon haluat raportit tallennettavan.")
    edited_save_dir = get_and_validate_path(save_path_guidance_text)

    return edited_save_dir


def get_and_validate_path(path_guidance_text):
    """Lukee käyttäjän syötteestä tiedostopolun ja tarkastaa, että se on
    olemassa ja että se johtaa hakemistoon."""

    while True:
        print(path_guidance_text)
        path = input()

        if not os.path.exists(path):
            print("Polkua ei olemassa.", file=stderr)
            continue

        if os.path.isfile(path):
            print(("Antamasi polku johti tiedostoon, mutta tarvitaan "
                    "hakemistoon johtava polku."), file=stderr)
            continue

        return path


def read_categories_tags():
    """Lukee käyttäjän aiemmin asettamat kategoriat ja niiden tunnisteet
    tunnistetiedostosta. Jos tunnistetiedosto on tyhjä, käyttäjää pyydetään
    asettamaan ne. Jos tunnistetiedosto ei ollut tyhjä, käyttäjältä kysytään,
    haluaako hän muuttaa niitä."""

    print("""Määritetään laskemisen kategoriat. Näihin kategorioihin
            tilitapahtumasi luokitellaan""")
    return set_categories_and_tags()


def set_categories_and_tags():
    """Kirjoittaa tilitapahtumien tarkastelussa käytettävät
    kategoriat ja niiden tunnistamiseen käytettävät tunnisteet."""

    categories = read_categories()

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan kuuluvat tunnisteet.
    tags = read_tags_for_categories(categories)

    return lists_to_dict(categories, tags)


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
