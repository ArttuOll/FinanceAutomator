"""Määrittelee luokan ReportWriter ja sen riippuvuudet"""
from datetime import datetime
from os.path import join
import json
from ..model.event_calculator import EventCalculator
from ..model.event_extractor import EventExtractor
from ..util.report_operations import sum_reports, average_reports
from .report_reader import ReportReader

class ReportWriter:
    """Huolehtii talousraporttien kirjoittamisesta ja tulostamisesta. Raportti
    kirjoitetaan konstruktorin parametrina annettavan
    values_by_category-sanakirjan perusteella. Raporttien tallennussijainti
    määritellään sanakirjaparametrin locations kohdassa "save" """

    def __init__(self, configs):
        self.configs = configs
        self.report_reader = ReportReader(configs["save_dir"])
        self.date_format = "%Y-%m-%d"
        self.timestamp = datetime.now().strftime(self.date_format)

    def write_report(self):
        event_extractor = EventExtractor()
        events = event_extractor.events_from_file(self.configs["transactions_dir"])
        event_calculator = EventCalculator(events, self.configs["categories_tags"])

        values_by_category = event_calculator.calculate_values()

        self._write_human_readable_report(values_by_category)
        self._write_machine_readable_report(values_by_category)

    def write_avg_report(self, start_date, end_date=""):
        title = f"fina_avg_from_{start_date}_to_{end_date}.txt"
        self._write_operation_report(start_date, average_reports, title, end_date)

    def write_sum_report(self, start_date, end_date=None):
        title = f"fina_sum_from_{start_date}_to_{end_date}.txt"
        self._write_operation_report(start_date, sum_reports, title, end_date)

    def _write_operation_report(self, start_date, operation_on_reports, title,
            end_date=None):
        reports = self.report_reader.read_in_time_period(start_date, end_date=end_date)
        results = operation_on_reports(reports)
        self._write_human_readable_report(results, title=title)

    def _write_human_readable_report(self, values_by_category, title=""):
        report = self._build_human_readable_report(values_by_category, title)
        filename = "fa_report.txt" if title in "" else title
        filepath = join(self.configs["save_dir"], filename)
        with open(filepath, "a", encoding="UTF-8") as human_readable_report:
            human_readable_report.write(report)

    def _build_human_readable_report(self, values_by_category, title):
        title = f"\nTalousraportti {self.timestamp}\n" if title in "" else f"\n{title}\n"
        report = title

        for category, value in values_by_category.items():
            report += f"{category}: {value}\n"

        return report

    def _print_human_readable_report(self, values_by_category, title=""):
        print(self._build_human_readable_report(values_by_category, title))

    def _write_machine_readable_report(self, values_by_category):
        filepath = join(self.configs["save_dir"], "fa_report_mr.txt")

        report_reader = ReportReader(self.configs["save_dir"])
        reports = report_reader.read_all_reports(filepath)

        new_report = self._build_machine_readable_report(values_by_category)
        reports.append(new_report)

        # default on funktio, joka ajetaan kaikille kohdattaville oliolle,
        # joita ei voida serialisoida!
        with open(filepath, "w", encoding="UTF-8") as report_file:
            json.dump(reports, report_file, ensure_ascii=False, indent=4, default=str)

    def _build_machine_readable_report(self, values_by_category):
        report_dict = values_by_category
        report_dict["timestamp"] = self.timestamp
        return report_dict
