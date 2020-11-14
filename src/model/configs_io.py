"""Huolehtii asetusten lukemisesta ja kirjoittamisesta asetustiedostoon, joka
sijaitsee käyttäjän kotikansiossa."""
import json
import os
from pathlib import Path


class ConfigsIO:
    """Kirjoittaa käyttäjän asettamat asetukset asetusolion määrittämään
    sijaintiin"""

    def __init__(self):
        self.file_name = ".fa_configs.json"
        self.configs_location = str(Path.home())
        self.location = os.path.join(self.configs_location, self.file_name)

    def write(self, configs):
        """Kirjoittaa asetukset JSON-muodossa käyttäjän kotikansioon
        tiedostonimellä 'fa_configs.json'"""

        with open(self.location, "w", encoding="UTF-8") as configs_file:
            json.dump(configs, configs_file, ensure_ascii=False, indent=4)

    def read(self):
        """Lukee asetustiedoston käyttäjän kotikansiosta ja palauttaa asetukset
        sanakirjana"""

        configs = {}
        try:
            with open(self.location, "r", encoding="UTF-8") as configs_file:
                data = configs_file.read()
                configs = json.loads(data)
        except IOError:
            print("""
                    Asetuksia ei ole asetettu.

                    Aseta asetukset joko manuaalisesti luomalla tiedosto nimeltä '.fa_configs.json'
                    kotikansioosi ja kirjoittamalla asetustiedosto ohjeiden mukaan 
                    (fa --config --help).

                    Vaihtoehtoisesti voit luoda asetustiedoston ohjastusti kutsumalla 
                    'fa --guided'.
                    """)

        return configs
