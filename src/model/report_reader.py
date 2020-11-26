"""Määrittelee luokan ReportReader ja sen riippuvuudet"""
import json
from datetime import datetime
from decimal import Decimal
from os.path import join


class ReportReader:
    """Lukee talousraportteja kansiossa save_dir tiedostosta fa_report_mr.txt
    ja laskee kategorioittan yhteen niiden arvot, tuottaen summaraportin.
    Raporttien lukeminen aloitetaan tuoreimmasta raportista ja jatkuu, kunnes
    löydetään raportti, jonka päivämäärä on pienempi kuin start_date."""

    # TODO: mahdollisuus lukea aikaväliltä
    # TODO: pitäisikö lukeminen ja yhteen laskeminen erottaa omiin olioihinsa?
    def __init__(self, save_dir):
        self.date_format = "%Y-%m-%d"
        self.location = join(save_dir, "fa_report_mr.txt")

    def read_from_date(self, start_date):
        """Lukee talousraportit sijannista self.location, suodattaa niistä
        sellaiset, joiden päivämäärä on ennen self.start_datea ja laskee niiden arvot
        kategorioittan yhteen, muodostaen summaraportin."""

        start_date = datetime.strptime(start_date, self.date_format).date()
        with open(self.location, "r", encoding="UTF-8") as reports_file:
            data = reports_file.read()
            all_reports = json.loads(data)
            self._format_reports(all_reports)
            reports_after_start_date = self._get_reports_after_start_date(all_reports, start_date)
            return self._sum_reports(reports_after_start_date)

    def _format_reports(self, reports):
        self._convert_timestamps_to_dates(reports)
        self._convert_strings_to_decimals(reports)

    def _convert_timestamps_to_dates(self, reports):
        for report in reports:
            date_string = report["timestamp"]
            date = datetime.strptime(date_string, self.date_format).date()
            report["timestamp"] = date

    @staticmethod
    def _convert_strings_to_decimals(reports):
        for report in reports:
            for key, value in report.items():
                if key not in "timestamp":
                    report[key] = Decimal(value)

    @staticmethod
    def _get_reports_after_start_date(reports, start_date):
        reports_after_start_date = []
        for report in reversed(reports):
            if report["timestamp"] >= start_date:
                reports_after_start_date.append(report)

        return reports_after_start_date

    @staticmethod
    def _sum_reports(reports):
        values_by_category = reports[0]
        values_by_category.pop("timestamp")

        for i, report in enumerate(reports):
            if i == 0:
                continue

            report.pop("timestamp")

            for key, value in report.items():
                values_by_category[key] += value

        return values_by_category
