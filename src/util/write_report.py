"""Määrittelee funktion write_report ja sen riippuvuudet"""
from ..model.event_calculator import EventCalculator
from ..model.event_extractor import EventExtractor
from ..model.report_writer import ReportWriter
from ..model.report_reader import ReportReader
from ..model.report_calculator import ReportCalculator


def write_report(locations, categories_tags, print_output=False):
    """Lukee tiliotteen sanakirjan locations kohtaa "transactions" vastaavasta
    kohdasta ja käyttää kategorioita ja niiden tunnisteita kategoriakohtaisten
    arvojen laskemiseen. Tämän jälkeen tuotetaan raportti, joka tallennetaan
    sanakirjan locations avaimen "save":a vastaavaan sijaintiin. Tähän
    sijantiin kirjoitetaan sekä ihmis- että koneluettava raportti."""

    event_extractor = EventExtractor()
    events = event_extractor.events_from_file(locations["transactions"])
    event_calculator = EventCalculator(events, categories_tags)

    values_by_category = event_calculator.calculate_values()
    report_writer = ReportWriter(values_by_category, locations["save"])

    report_writer.write_human_readable_report()
    report_writer.write_machine_readable_report()

    if print_output:
        report_writer.print_human_readable_report()

def write_analytical_report(operation, start_date, save_dir, print_output=False, end_date=""):
    """Lukee raportit sijainnista save_dir ja laskee sellaisten raporttien
    arvot kategorioittain yhteen, joiden päivämäärä on start_daten ja end_daten
    välissä (molemmat itse mukaanluettuina). Jos end_datea ei ole annettu,
    luetaan kaikki raportit start_datesta tulevaisuuteen. Tulokset kirjoitetaan
    sijaintiin save_dir."""

    report_reader = ReportReader(save_dir)
    reports = report_reader.read_in_time_period(start_date, end_date=end_date)
    report_calculator = ReportCalculator(reports)
    if operation in "sum":
        title = f"fa_report_sum_{start_date}_{end_date}.txt"
        values_by_category = report_calculator.sum_reports()
        report_writer = ReportWriter(values_by_category, save_dir)
        report_writer.write_human_readable_report(title=title)

        if print_output:
            report_writer.print_human_readable_report(title)

    if operation in "avg":
        title = f"fa_report_avg_{start_date}_{end_date}.txt"
        values_by_category = report_calculator.average_reports()
        report_writer = ReportWriter(values_by_category, save_dir)
        report_writer.write_human_readable_report(title=title)

        if print_output:
            report_writer.print_human_readable_report(title)
