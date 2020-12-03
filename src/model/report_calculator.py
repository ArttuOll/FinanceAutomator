"""Määrittelee luokan ReportCalculator ja sen riippuvuudet"""

class ReportCalculator:
    """Suorittaa laskutoimenpiteitä raporteille kategorioittain"""

    def __init__(self, reports):
        self.reports = reports
        self.values_by_category = reports[0]
        self.values_by_category.pop("timestamp")

    def sum_reports(self):
        """Laskee raportteja kategorioittain yhteen ja palauttaa tulokset
        sanakirjana."""

        sum_report = self.values_by_category.copy()

        for i, report in enumerate(self.reports):
            if i == 0:
                continue

            report.pop("timestamp")

            for key, value in report.items():
                sum_report[key] += value

        return sum_report

    def average_reports(self):
        """Laskee raporteille kategorioittain keskiarvon ja palauttaa tulokset
        sanakirjana."""

        average_report = self.values_by_category.copy()

        for i, report in enumerate(self.reports):
            if i == 0:
                continue

            report.pop("timestamp")

            # TODO: keskiarvon laskeminen
            for key, value in report.items():
                average_report[key] += value

        return average_report
