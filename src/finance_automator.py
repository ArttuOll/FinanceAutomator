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

@cli.command(short_help="Lukee tilitapahtumat ja kirjoittaa niistä raportin.")
@click.argument("transactions_file")
@pass_configs
def read(configs, transactions_file):
    configs.set_config("transactions_file", transactions_file)
    report_writer = ReportWriter(configs)
    report_writer.write_report()

@cli.command()
@click.argument("start_date")
@click.option("--end", help="Loppupäivämäärä")
@click.option("--title", help="Raporttitiedoston nimi", default="")
@pass_configs
def sum(configs, start_date, end, title):
    report_writer = ReportWriter(configs)
    report_writer.write_sum_report(start_date, end_date=end, title=title)

@cli.command()
@click.argument("start_date")
@click.option("--end", help="Loppupäivämäärä")
@click.option("--title", help="Raporttitiedoston nimi", default="")
@pass_configs
def avg(configs, start_date, end, title):
    report_writer = ReportWriter(configs)
    report_writer.write_avg_report(start_date, end_date=end, title=title)
