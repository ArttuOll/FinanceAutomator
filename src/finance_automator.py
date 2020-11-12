"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3

from sys import argv
from .model.guided_configuration import guided_configuration
from .model.settings_writer import SettingsWriter

GUIDED_CONFIG_SHORT = "-g"
GUIDED_CONFIG = "--guided"

main_argument = argv[1]

if main_argument in GUIDED_CONFIG_SHORT or main_argument in GUIDED_CONFIG:
    settings = guided_configuration()
    settings_writer = SettingsWriter(settings)
    settings_writer.write()
