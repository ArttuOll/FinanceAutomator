"""Määrittelee luokan ReportCalculator ja sen riippuvuudet"""

def sum_reports(reports):
    """Laskee raportteja kategorioittain yhteen ja palauttaa tulokset
    sanakirjana."""

    template = reports.copy()
    sum_report = {}

    for report in template:
        report.pop("timestamp")

        for key, value in report.items():
            sum_report[key] += value

    return sum_report

def average_reports(reports):
    """Laskee raporteille kategorioittain keskiarvon ja palauttaa tulokset
    sanakirjana."""

    template = reports.copy()
    average_report = {}

    for report in template:
        report.pop("timestamp")

        # TODO: keskiarvon laskeminen
        for key, value in report.items():
            average_report[key] += value

    return average_report
