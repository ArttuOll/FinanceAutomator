"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3

from sys import argv
from .util.guided_configuration import guided_configuration
from .model.configs_io import ConfigsIO

GUIDED_CONFIG_SHORT = "-g"
GUIDED_CONFIG = "--guided"

main_argument = argv[1]

configs_io = ConfigsIO()
configs = configs_io.read()

if main_argument in GUIDED_CONFIG_SHORT or main_argument in GUIDED_CONFIG:
    guided_configuration()
