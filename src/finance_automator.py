"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

from sys import argv, exit as sysexit
from .util.guided_configuration import guided_configuration
from .model.configs_io import ConfigsIO
from .util.help import show_help

GUIDED_CONFIG_SHORT = "-g"
GUIDED_CONFIG = "--guided"

HELP_SHORT = "-h"
HELP = "--help"

main_argument = argv[1]

if main_argument in GUIDED_CONFIG_SHORT or main_argument in GUIDED_CONFIG:
    guided_configuration()
    sysexit()
elif main_argument in HELP_SHORT or main_argument in HELP:
    show_help()
    sysexit()

configs_io = ConfigsIO()
configs = configs_io.read()
if configs:
    print(configs)
