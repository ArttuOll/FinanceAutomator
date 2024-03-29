"""Sovelluksen päätiedosto. Tulkitsee komentoriviparametrit ja kutsuu niitä
vastaavia funkioita. Lukee asetukset asetustiedostosta."""

import click

from .model.configs import Configs
from .util.guided_configuration import guided_configuration
from .model.report_writer import ReportWriter
from .model.graph_drawer import GraphDrawer

# Luo uuden dekoraattorin, jota voidaan käyttää configs-olion tarjoamiseksi sitä tarvitseville
# komennoille. ensure=True luo configs-olion, jos sitä ei ole tätä dekoraattoria käytettäessä vielä
# olemassa
pass_configs = click.make_pass_decorator(Configs, ensure=True)

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Lisää ulostulon määrää")
@click.pass_context
def cli(context, verbose):
    context.obj = Configs()
    context.obj.read()
    context.obj.set_config("verbose", verbose)

@cli.command(short_help="Suorita ohjattu asetustiedoston luominen")
def guided_config():
    guided_configuration()

@cli.command(short_help="Lue tilitapahtumatiedosto ja kirjoita siitä raportti")
@click.argument("transactions_file", type=click.Path(exists=True))
@pass_configs
def read(configs, transactions_file):
    configs.set_config("transactions_file", transactions_file)
    report_writer = ReportWriter(configs)
    report_writer.write_report()

@cli.command(short_help="Laske kulu- ja menokategorioiden arvoja yhteen aikavälillä")
@click.argument("start_date")
@click.option("--end", help="Aikavälin loppupäivämäärä")
@click.option("--title", help="Kirjoitettavan raporttitiedoston nimi", default="")
@pass_configs
def sum(configs, start_date, end, title):
    report_writer = ReportWriter(configs)
    report_writer.write_sum_report(start_date, end_date=end, title=title)

@cli.command(short_help="Laske kulu- ja menokategorioiden keskiarvot aikaväliä kohti")
@click.argument("start_date")
@click.option("--end", help="Loppupäivämäärä")
@click.option("--title", help="Kirjoitettavan raporttitiedoston nimi", default="")
@pass_configs
def avg(configs, start_date, end, title):
    report_writer = ReportWriter(configs)
    report_writer.write_avg_report(start_date, end_date=end, title=title)

@cli.command(short_help="Piirrä kuvaaja kategorian arvoista aikavälillä")
@click.argument("start_date")
@click.argument("category")
@click.option("--end", help="Aikavälin loppupäivämäärä")
@pass_configs
def graph(configs, start_date, category, end):
    graph_drawer = GraphDrawer(configs)
    graph_drawer.draw(start_date, category, end)

@cli.command(short_help="Tulosta tulot, menot ja säästöt JSON-taulukkona.")
@click.argument("transactions_file", type=click.Path(exists=True))
@pass_configs
def export(configs, transactions_file):
    configs.set_config("transactions_file", transactions_file)
    report_writer = ReportWriter(configs)
    print(report_writer.export_event_types_as_json())
