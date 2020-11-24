"""Määrittelee luokan ReportWriter ja sen riippuvuudet"""
from datetime import datetime
from os.path import join
import json

class ReportWriter:
    """Huolehtii talousraporttien kirjoittamisesta ja tulostamisesta. Raportti
    kirjoitetaan konstruktorin parametrina annettavan
    values_by_category-sanakirjan perusteella. Raporttien tallennussijainti
    määritellään sanakirjaparametrin locations kohdassa "save" """

    def __init__(self, values_by_category, locations):
        self.values_by_category = values_by_category
        self.save_location = locations["save"]
        self.timestamp = datetime.now()

    def write_human_readable_report(self):
        """Kirjoittaa raportin selkokielisenä käyttäjän määrittämään
        tallennuskansioon tiedostonimellä "fa_report.txt". Uudet raportit
        kirjoitetaan aina samaan tiedostoon. """

        report = self._build_human_readable_report()
        filename = join(self.save_location, "fa_report.txt")
        with open(filename, "a", encoding="UTF-8") as human_readable_report:
            human_readable_report.write(report)

    def _build_human_readable_report(self):
        report = f"Talousraportti {self.timestamp}\n"

        for category, value in self.values_by_category.items():
            report += f"{category}: {value}\n"

        return report

    def print_human_readable_report(self):
        """Tulostaa raportin."""

        print(self._build_human_readable_report())

    def write_machine_readable_report(self):
        """Kirjoittaa raportin JSON-muodossa käyttäjän määrittämään
        tallennuskansioon tiedostonimellä "fa_report_mr.txt". Uudet raportit
        kirjoitetaan aina samaan tiedostoon."""

        filename = join(self.save_location, "fa_report_mr.txt")

        reports = self._read_reports(filename)

        new_report = self._build_machine_readable_report()
        reports.append(new_report)
        # default on funktio, joka ajetaan kaikille kohdattaville oliolle,
        # joita ei voida serialisoida!
        with open(filename, "a", encoding="UTF-8") as report_file:
            json.dump(reports, report_file, ensure_ascii=False, indent=4, default=str)

    def _build_machine_readable_report(self):
        report_dict = self.values_by_category
        report_dict["timestamp"] = self.timestamp
        return report_dict

    def _read_reports(self, filename):
        try:
            with open(filename, "r", encoding="UTF-8") as report_file:
                data = report_file.read()
                return json.loads(data)
        except IOError:
            print("""Raporttitiedostoa ei löytynyt tallennussijainnista. Joko
                  sitä ei ole vielä luotu tai se on siirretty.""")
            return []
