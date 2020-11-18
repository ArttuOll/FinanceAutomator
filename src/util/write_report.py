"""Määrittelee funktion write_report ja sen riippuvuudet"""
from ..model.event_calculator import EventCalculator
from ..model.event_extractor import EventExtractor
from ..model.report_writer import ReportWriter


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
    report_writer = ReportWriter(values_by_category, locations)

    # report_writer.write_human_readable_report()
    # report_writer.write_machine_readable_report()

    if print_output:
        report_writer.print_human_readable_report()
