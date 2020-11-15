"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

from argparse import ArgumentParser
from .util.guided_configuration import guided_configuration
from .model.configs_io import ConfigsIO
from .util.write_report import write_report

def handle_commands_not_requiring_settings(args):
    """Hoitaa sellaisten komentojen tulkinnan, jotka eivät vaadi tietoa
    ohjelman asetuksista. Tämän funktion suorittamisen jälkeen ohjelma poistuu"""

    if args.guided:
        guided_configuration()


def handle_commands_requiring_settings(configs_object, args):
    """Hoitaa sellaisten komentojen tulkinnan, jotka vaativat tiedon ohjelman
    asetuksista. Antaa kutsumilleen funktioille niiden vaatimat asetukset
    argumenttina. Tätä funktiota kutsutaan vain, jos asetukset on pystytty
    lukemaan onnistuneesti. Tämän funktion suorittamisen jälkeen ohjelma poistuu"""

    if args.report:
        saving_location = configs_object["save_dir"]
        categories_tags = configs_object["categories_tags"]
        write_report(saving_location, categories_tags)


argument_parser = ArgumentParser()
argument_parser.add_argument("-g", "--guided", action="store_true",
                            help="Suorita ohjattu asetustiedoston luonti")
argument_parser.add_argument("-r", "--report", action="store_true",
                            help="""Kirjoittaa raportin viime kuukauden tilitapahtumista
                                    tallennuskansiossa sijaitsevaan raporttitiedostoon.""")

arguments = argument_parser.parse_args()

handle_commands_not_requiring_settings(arguments)

configs_io = ConfigsIO()
configs = configs_io.read()
if configs:
    handle_commands_requiring_settings(configs, arguments)
