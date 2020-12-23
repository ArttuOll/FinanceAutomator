"""Määrittelee luokan ReportReader ja sen riippuvuudet"""
import json
from datetime import datetime
from decimal import Decimal
from os.path import join
from sys import stderr


class ReportReader:
    """Lukee talousraportteja kansiossa save_dir tiedostosta fa_report_mr.txt
    ja laskee kategorioittan yhteen niiden arvot, tuottaen summaraportin.
    Raporttien lukeminen aloitetaan tuoreimmasta raportista ja jatkuu, kunnes
    löydetään raportti, jonka päivämäärä on pienempi kuin start_date."""

    def __init__(self, save_dir):
        self.date_format = "%Y-%m-%d"
        self.location = join(save_dir, "fina_reports_mr.txt")
        self.max_date = "3000-1-1"

    def get_category_values_in_time_period(self, start_date, category, end_date=None):
        end_date = end_date if end_date is not None else self.max_date
        reports_in_time_period = self.read_in_time_period(start_date, end_date)
        category_values_in_time_period = []
        for report in reports_in_time_period:
            category_values_in_time_period.append(report[category])

        return category_values_in_time_period

    def read_in_time_period(self, start_date, end_date=None):
        """Lukee talousraportit sijannista self.location, suodattaa niistä
        sellaiset, joiden päivämäärä on start_daten ja end_daten välissä ja
        laskee niiden arvot kategorioittan yhteen, muodostaen summaraportin.
        Jos end_datea ei ole annettu, luetaan raportit tuoreimpaan asti."""

        start_date = datetime.strptime(start_date, self.date_format).date()
        end_date = self._parse_end_date(end_date)
        all_reports = self.read_all_reports(self.location)
        return self._filter_reports_by_time_period(all_reports, start_date, end_date=end_date)

    @staticmethod
    def _filter_reports_by_time_period(reports, start_date, end_date):
        report_in_time_period = lambda report: start_date <= report["timestamp"] <= end_date
        return list(filter(report_in_time_period, reports))

    def _parse_end_date(self, end_date):
        if end_date:
            end_date = datetime.strptime(end_date, self.date_format).date()
        else:
            end_date = datetime.strptime(self.max_date, self.date_format).date()
        return end_date

    def read_all_reports(self, location):
        """Lukee ja palauttaa raportit parametrin location osoittamasta
        sijainnista."""

        try:
            with open(location, "r", encoding="UTF-8") as reports_file:
                data = reports_file.read()
                all_reports = json.loads(data)
                self._format_reports(all_reports)
                return all_reports

        except IOError:
            print("""Raporttitiedostoa ei löytynyt tallennussijainnista. Joko
                  sitä ei ole vielä luotu tai se on siirretty. Jos tämä on
                  ohjelman ensimmäinen suorituskerta, kaikki on hyvin.""", file=stderr)
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
