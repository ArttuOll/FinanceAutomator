from os.path import join

class ReportCalculator:
    def __init__(self, reports):
        self.reports = reports

    def sum_reports(self):
        values_by_category = self.reports[0]
        values_by_category.pop("timestamp")

        for i, report in enumerate(self.reports):
            if i == 0:
                continue

            report.pop("timestamp")

            for key, value in report.items():
                values_by_category[key] += value

        return values_by_category
