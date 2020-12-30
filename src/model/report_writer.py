"""Määrittelee luokan ReportWriter ja sen riippuvuudet"""
import json
from datetime import datetime
from os.path import join
from sys import stderr

from ..model.event_calculator import EventCalculator
from ..model.event_extractor import EventExtractor
from ..util.report_operations import average_reports, sum_reports
from .report_reader import ReportReader
from ..util.report_builders import build_human_readable_report, build_machine_readable_report


class ReportWriter:
    """Huolehtii talousraporttien kirjoittamisesta ja tulostamisesta."""

    def __init__(self, configs):
        self.configs = configs
        self.report_reader = ReportReader(configs.get_config("save_dir"))
        self.date_format = "%Y-%m-%d"
        self.timestamp = datetime.now().strftime(self.date_format)

    def write_report(self):
        """Kirjoittaa ihmis- ja koneluettavan raportin asetuksien kohdassa 'save_dir' määritettyyn
        tallennushakemistoon."""

        values_by_category = self._get_values_by_category()
        self._write_human_readable_report(values_by_category)
        self._write_machine_readable_report(values_by_category)

        if self.configs.verbose:
            self._print_human_readable_report(values_by_category)

    def _get_values_by_category(self):
        event_extractor = EventExtractor()
        transactions_file = self.configs.get_config("transactions_file")
        events = event_extractor.extract_events_from_file(transactions_file)

        categories_tags = self.configs.get_config("categories_tags")
        event_calculator = EventCalculator(events, categories_tags)
        return event_calculator.calculate_values()

    def write_avg_report(self, start_date, end_date="", title=""):
        """Kirjoittaa raportin, joka sisältää kunkin kulu- ja menokategorian keskiarvot aikavälillä
        [start_date, end_date] laskettuna. Raportti tallennetaan asetusten kohdassa 'save_dir'
        määritettyyn hakemistoon"""

        title = title if title not in "" else self._get_title("avg", start_date, end_date)
        self._write_operation_report(start_date, average_reports, title, end_date)

    def write_sum_report(self, start_date, end_date=None, title=""):
        """Kirjoittaa raportin, joka sisältää kunkin kulu- ja menokategorian summan aikavälillä
        [start_date, end_date] laskettuna. Raportti tallennetaan asetusten kohdassa 'save_dir'
        määritettyyn hakemistoon"""

        title = title if title not in "" else self._get_title("sum", start_date, end_date)
        self._write_operation_report(start_date, sum_reports, title, end_date=end_date)

    @staticmethod
    def _get_title(operation, start_date, end_date):
        now = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        title = f"fina_{operation}_from_{start_date}_to_{now}.txt"
        if end_date is not None:
            title = f"fina_{operation}_from_{start_date}_to_{end_date}.txt"

        return title

    def _write_operation_report(self, start_date, operation_on_reports, title, end_date=None):
        reports = self.report_reader.read_in_time_period(start_date, end_date=end_date)
        results = operation_on_reports(reports)
        self._write_human_readable_report(results, title=title)

        if self.configs.verbose:
            self._print_human_readable_report(results, title=title)

    def _write_human_readable_report(self, values_by_category, title=""):
        report = build_human_readable_report(self.timestamp, values_by_category, title)
        filename = title if title not in "" else "fina_reports.txt"
        filepath = join(self.configs.get_config("save_dir"), filename)
        try:
            with open(filepath, "a", encoding="UTF-8") as human_readable_report:
                human_readable_report.write(report)
        except IOError as error:
            print("Virhe yritettäessä kirjoittaa ihmisluettavaa raporttia: ", error, file=stderr)


    def _print_human_readable_report(self, values_by_category, title=""):
        print(build_human_readable_report(self.timestamp, values_by_category, title))

    def _write_machine_readable_report(self, values_by_category):
        filepath = join(self.configs.get_config("save_dir"), "fina_reports_mr.txt")

        reports = self.report_reader.read_all_reports(filepath)

        new_report = build_machine_readable_report(self.timestamp, values_by_category)
        reports.append(new_report)

        # default on funktio, joka ajetaan kaikille kohdattaville oliolle,
        # joita ei voida serialisoida!
        try:
            with open(filepath, "w", encoding="UTF-8") as report_file:
                json.dump(reports, report_file, ensure_ascii=False, indent=4, default=str)
        except IOError as error:
            print("Virhe yritettäessä kirjoittaa koneluettavaa raporttia: ", error, file=stderr)
