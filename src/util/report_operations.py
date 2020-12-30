"""Määrittelee laskutoimitusten raporteilla suorittamiseksi vaadittavat funktiot"""

def sum_reports(reports):
    """Laskee raportteja kategorioittain yhteen ja palauttaa tulokset sanakirjana."""

    sum_report = reports[0]
    sum_report.pop("timestamp")
    for i, report in enumerate(reports):
        # Ensimmäinen alkio on sisällytetty jo sum_reportiin!
        if i == 0:
            continue

        report.pop("timestamp")

        for key, value in report.items():
            sum_report[key] += value

    return sum_report

def average_reports(reports):
    """Laskee raporteille kategorioittain keskiarvon ja palauttaa tulokset sanakirjana."""

    average_report = sum_reports(reports)
    for key in average_report.keys():
        average = average_report[key] / len(reports)
        average_report[key] = average

    return average_report
