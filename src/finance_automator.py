"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

from sys import argv, exit as sysexit
from .util.guided_configuration import guided_configuration
from .model.configs_io import ConfigsIO
from .util.help import show_help
from .util.write_report import write_report

def handle_commands_not_requiring_settings(command):
    """Hoitaa sellaisten komentojen tulkinnan, jotka eivät vaadi tietoa
    ohjelman asetuksista. Tämän funktion suorittamisen jälkeen ohjelma poistuu"""

    if command in GUIDED_CONFIG_SHORT or command in GUIDED_CONFIG:
        guided_configuration()
    elif command in HELP_SHORT or command in HELP:
        show_help()

    sysexit()


def handle_commands_requiring_settings(configs_object, command):
    """Hoitaa sellaisten komentojen tulkinnan, jotka vaativat tiedon ohjelman
    asetuksista. Antaa kutsumilleen funktioille niiden vaatimat asetukset
    argumenttina. Tätä funktiota kutsutaan vain, jos asetukset on pystytty
    lukemaan onnistuneesti. Tämän funktion suorittamisen jälkeen ohjelma poistuu"""

    if command in REPORT_SHORT or command in REPORT:
        saving_location = configs_object["save_dir"]
        categories_tags = configs_object["categories_tags"]
        write_report(saving_location, categories_tags)

    sysexit()


GUIDED_CONFIG_SHORT = "-g"
GUIDED_CONFIG = "--guided"

HELP_SHORT = "-h"
HELP = "--help"

REPORT_SHORT = "-r"
REPORT= "--report"

main_argument = argv[1]

handle_commands_not_requiring_settings(main_argument)

configs_io = ConfigsIO()
configs = configs_io.read()
if configs:
    handle_commands_requiring_settings(configs, main_argument)
