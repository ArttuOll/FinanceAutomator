"""Huolehtii asetusten lukemisesta ja kirjoittamisesta asetustiedostoon, joka
sijaitsee käyttäjän kotikansiossa."""
import json
from os import path
from sys import stderr
from pathlib import Path


class Configs:
    """Kirjoittaa käyttäjän asettamat asetukset asetusolion määrittämään
    sijaintiin"""

    def __init__(self):
        self.file_name = ".fina_configs.json"
        self.configs_location = str(Path.home())
        self.location = path.join(self.configs_location, self.file_name)
        self.configs = {}

    def write(self):
        """Kirjoittaa asetukset JSON-muodossa käyttäjän kotikansioon
        tiedostonimellä '.fina_configs.json'"""

        try:
            with open(self.location, "w", encoding="UTF-8") as configs_file:
                json.dump(self.configs, configs_file, ensure_ascii=False, indent=4)
        except IOError as error:
            print("Virhe yritettäessä kirjoittaa asetuksia: ", error, file=stderr)

    def read(self):
        """Lukee asetustiedoston käyttäjän kotikansiosta ja palauttaa asetukset
        sanakirjana"""

        try:
            with open(self.location, "r", encoding="UTF-8") as configs_file:
                data = configs_file.read()
                self.configs = json.loads(data)
        except IOError:
            print("""
                    Asetuksia ei ole asetettu.

                    Aseta asetukset joko manuaalisesti luomalla tiedosto nimeltä '.fa_configs.json'
                    kotikansioosi ja kirjoittamalla asetustiedosto ohjeiden mukaan 
                    (fa --config --help).

                    Vaihtoehtoisesti voit luoda asetustiedoston ohjastusti kutsumalla 
                    'fa --guided'.
                    """, file=stderr)

    def get_config(self, key):
        return self.configs.get(key)

    def set_config(self, key, value):
        self.configs[key] = value
