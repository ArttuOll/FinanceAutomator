"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

import click

from .model.configs import Configs
from .util.guided_configuration import guided_configuration
from .model.report_writer import ReportWriter

pass_configs = click.make_pass_decorator(Configs, ensure=True)

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Lisää ulostulon määrää")
@click.pass_context
def cli(context, verbose):
    context.obj = Configs()
    context.obj.verbose = verbose
    context.obj.read()

@cli.command()
def guided_config():
    guided_configuration()

# TODO: lisää luettavan tiedoston sijainti parametriksi ja poista
# transactions_dir asetustiedostosta
@cli.command(short_help="Lukee tilitapahtumat ja kirjoittaa niistä raportin.")
@pass_configs
def read(configs):
    report_writer = ReportWriter(configs)
    report_writer.write_report()

@cli.command()
@click.option("--end", help="Loppupäivämäärä")
@click.argument("start_date")
@pass_configs
def sum(configs, start_date, end):
    report_writer = ReportWriter(configs)
    report_writer.write_sum_report(start_date, end_date=end)
