"""Huolehtii tunnisteiden lukemisesta ja kirjoittamisesta tunnistetiedostoon."""
import json
import os


class ConfigsIO:
    """Kirjoittaa käyttäjän asettamat asetukset asetusolion määrittämään
    sijaintiin"""
    def __init__(self, configs):
        self.file_name = ".fa_configs.json"
        self.configs = configs
        self.configs_location = configs["configs_dir"]

    def write(self):
        """Kirjoittaa asetukset JSON-muodossa ennalta määritettyyn sijaintiin
        tiedostonimellä 'fa_configs.json'"""
        with open(self.file_name, "w", encoding="UTF-8") as configs_file:
            json.dump(self.configs, configs_file, ensure_ascii=False, indent=4)

        url = os.path.join(self.configs_location, self.file_name)
        os.rename(self.file_name, url)
