"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

import click

from .model.configs_io import ConfigsIO
from .util.guided_configuration import guided_configuration
from .model.report_writer import ReportWriter

@click.group()
@click.pass_context
def cli(context):
    # Siltä varalta, että cli:tä kutsutaan muualta kuin tämän tiedoston alaosan
    # if-blokista
    context.ensure_object(dict)

    configs_io = ConfigsIO()
    context.obj = configs_io.read()

@cli.command()
def guided_config():
    guided_configuration()

# TODO: lisää luettavan tiedoston sijainti parametriksi ja poista
# transactions_dir asetustiedostosta
@cli.command(short_help="Lukee tilitapahtumat ja kirjoittaa niistä raportin.")
@click.pass_context
def read(context):
    report_writer = ReportWriter(context.obj)
    report_writer.write_report()

@cli.command()
@click.pass_context
@click.argument("start_date")
def sum(context, start_date):
    report_writer = ReportWriter(context.obj)
    report_writer.write_sum_report(start_date)
