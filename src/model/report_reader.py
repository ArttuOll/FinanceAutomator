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
    def __init__(self, save_dir):
        self.date_format = "%Y-%m-%d"
        self.location = join(save_dir, "fa_report_mr.txt")

    def read_from_date(self, start_date):
        """Lukee talousraportit sijannista self.location, suodattaa niistä
        sellaiset, joiden päivämäärä on ennen self.start_datea ja laskee niiden arvot
        kategorioittan yhteen, muodostaen summaraportin."""

        start_date = datetime.strptime(start_date, self.date_format).date()
        all_reports = self.read_all_reports(self.location)
        return self._get_reports_after_start_date(all_reports, start_date)

    def read_all_reports(self, location):
        try:
            with open(location, "r", encoding="UTF-8") as reports_file:
                data = reports_file.read()
                all_reports = json.loads(data)
                self._format_reports(all_reports)
                return all_reports

        except IOError:
            print("""Raporttitiedostoa ei löytynyt tallennussijainnista. Joko
                  sitä ei ole vielä luotu tai se on siirretty.""")
            return []


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
