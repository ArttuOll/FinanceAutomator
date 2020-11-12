"""Huolehtii tunnisteiden lukemisesta ja kirjoittamisesta tunnistetiedostoon."""
import json
import os


class SettingsWriter:
    """Kirjoittaa käyttäjän asettamat asetukset asetusolion määrittämään
    sijaintiin"""
    def __init__(self, settings):
        self.file_name = "fa_settings.json"
        self.settings = settings
        self.settings_location = settings[0]

    def write(self):
        """Kirjoittaa asetukset JSON-muodossa ennalta määritettyyn sijaintiin
        tiedostonimellä 'fa_settings.json'"""
        with open(self.file_name, "w", encoding="UTF-8") as settings_file:
            json.dump(self.settings, settings_file, ensure_ascii=False, indent=4)

        url = os.path.join(self.settings_location, self.file_name)
        os.rename(self.file_name, url)
