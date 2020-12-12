"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

import click

from .model.configs_io import ConfigsIO
from .util.guided_configuration import guided_configuration
from .util.write_report import write_report

@click.group()
def cli():
    pass

@click.command()
def guided_config():
    guided_configuration()

# TODO: lisää luettavan tiedoston sijainti parametriksi ja poista
# transactions_dir asetustiedostosta
@click.command()
def read():
    configs_io = ConfigsIO()
    configs = configs_io.read()
    write_report(configs)

if __name__ == "__main__":
    cli.add_command(guided_config)
    cli.add_command(read)
    cli()
