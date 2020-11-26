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
    # TODO: jos sekä start_date että end_date annettu, lue niiden väliltä. Jos
    # vain start_date annettu, lue siitä tuoreimpaan
    report_reader = ReportReader(save_dir)
    if operation in "sum":
        title = f"fa_report_sum_{start_date}_{end_date}"
        values_by_category = []
        if start_date and not end_date:
            reports = report_reader.read_from_date(start_date)
            report_calculator = ReportCalculator()
            values_by_category = report_calculator.sum_reports(reports)

        report_writer = ReportWriter(values_by_category, save_dir)
        report_writer.write_human_readable_report(title=title)

        if print_output:
            print(report_writer.print_human_readable_report())
