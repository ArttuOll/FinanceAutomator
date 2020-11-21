from datetime import datetime
from os.path import join
from decimal import Decimal
import json

class ReportWriter:

    def __init__(self, values_by_category, locations):
        self.values_by_category = values_by_category
        self.save_location = locations["save"]
        self.transactions_location = locations["transactions"]
        self.timestamp = datetime.now()

    def write_human_readable_report(self):
        report = self._build_human_readable_report()
        filename = join(self.save_location, "fa_report.txt")
        with open(filename, "w", encoding="UTF-8") as human_readable_report:
            human_readable_report.write(report)

    def _build_human_readable_report(self):
        report = f"Talousraportti {self.timestamp}\n"

        for category, value in self.values_by_category.items():
            report += f"{category}: {value}\n"

        return report

    def print_human_readable_report(self):
        print(self._build_human_readable_report())

    def write_machine_readable_report(self):
        report = self._build_machine_readable_report()
        filename = join(self.save_location, "fa_report_mr.txt")
        # default on funktio, joka ajetaan kaikille kohdattaville oliolle,
        # joita ei voida serialisoida!
        with open(filename, "a", encoding="UTF-8") as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=4, default=str)

    def _build_machine_readable_report(self):
        report_dict = self.values_by_category
        report_dict["timestamp"] = self.timestamp
        return report_dict
