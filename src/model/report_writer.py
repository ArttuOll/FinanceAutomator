from datetime import datetime
from os.path import join

class ReportWriter:

    def __init__(self, values_by_category, locations):
        self.values_by_category = values_by_category
        self.save_location = locations["save"]
        self.transactions_location = locations["transactions"]
        self.timestamp = datetime.now()

    def write_human_readable_report(self):
        report = self.build_human_readable_report()
        filename = join(self.save_location, "fa_report.txt")
        with open(filename, "w", encoding="UTF-8") as human_readable_report:
            human_readable_report.write(report)

    def build_human_readable_report(self):
        report = f"\nTalousraportti {self.timestamp}\n"

        for category, value in self.values_by_category.items():
            report += f"{category}: {value}\n"

        return report

    def print_human_readable_report(self):
        print(self.build_human_readable_report())
