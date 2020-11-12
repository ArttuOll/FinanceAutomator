"""Sovelluksen pääohjelma. Sisältää käyttöliittymän ja sen riippuvuudet."""
#!/usr/bin/env python3

from sys import argv
from .model.guided_configuration import guided_configuration
from .model.configs_writer import ConfigsWriter

GUIDED_CONFIG_SHORT = "-g"
GUIDED_CONFIG = "--guided"

main_argument = argv[1]

if main_argument in GUIDED_CONFIG_SHORT or main_argument in GUIDED_CONFIG:
    configs = guided_configuration()
    configs_writer = ConfigsWriter(configs)
    configs_writer.write()
