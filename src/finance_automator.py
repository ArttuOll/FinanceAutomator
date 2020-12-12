"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

import click

from .model.configs_io import ConfigsIO
from .util.guided_configuration import guided_configuration
from .util.parse_arguments import parse_arguments

@click.command
def guided_config():
    guided_configuration()

def main():
    arguments = parse_arguments()

    # Komennot, jotka tarvitsevat asetuksia
    if arguments.guided:
        guided_configuration()

    # Komennot, jotka eivät tarvitse asetuksia
    configs_io = ConfigsIO()
    configs = configs_io.read()
    if configs:
        arguments.func(configs, arguments)


if __name__ == "__main__":
    main()
