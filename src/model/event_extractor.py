"""Määrittelee luokan EventExtractor ja sen käyttämät apufunktiot."""
from os import listdir
from os.path import isfile, join
from sys import stderr

from ..model.event import Event


def clean_fragments(unclean_fragments):
    """Muuttaa tilitapahtumamerkkijonon osat helpommin käsiteltävään muotoon.
    Kaikki heittomerkit poistetaan ja desimaalipilkut korvataan pisteillä."""
    fragments = []
    for fragment in unclean_fragments:
        fragment = fragment.strip("\"").strip("\'")

        if "," in fragment:
            fragment = fragment.replace(",", ".")

        fragments.append(fragment)

    return fragments


class EventExtractor:
    """Lukee tilitapahtumat sisältävän tiedoston ja muuntaa sen Event-olioita
    sisältäväksi listaksi."""

    def events_from_file(self, path):
        """Hoitaa tilitapahtumat sisältävän tiedoston lukemisen ja Event-olioita
        sisältävän listan palauttamisen."""

        try:
            events_filename = self.__read_events_filename_from_directory(path)
            file = join(path, events_filename)
            return self.__read_events_from_file(file)
        except FileNotFoundError:
            print("Tiedostoa ei ole olemassa.", file=stderr)
            return None

    def __read_events_filename_from_directory(self, path):
        file = [f for f in listdir(path) if isfile(join(path, f))]
        if len(file) != 1:
            # TODO: tämä järjettömyys poistuu, kun read-komennolle voi antaa
            # tiedoston suoraan
            print("Tiliotteen sisältävässä kansiossa oli useampi kuin yksi tiedosto."
                  " Vain yhtä odotettiin. Poista muut tiedostot ja aja ohjelma uudelleen.")
            return None

        return file[0]

    def __read_events_from_file(self, file):
        events = []
        try:
            with open(file, "r", encoding="iso-8859-1") as events_file:
                all_lines = events_file.read().splitlines()

            # Delete header row
            lines = all_lines[1:]

            for line in lines:
                frags_unclean = line.split(";")
                frags = clean_fragments(frags_unclean)
                events.append(self.__create_event(frags))
        except IOError as error:
            print("Virhe yritettäessä lukea tilitapahtumia tiedostosta: ", error, file=stderr)


        return events

    def __create_event(self, fragments):
        """Luo ja palauttaa oikean tyyppisen Event-olion perustuen
        tilitapahtumatiedostossa määriteltyyn tapahtumatyyppiin."""

        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]

        event_types = {
                "KORTTIOSTO": self._create_card_payment_event,
                "PALKKA": self._create_salary_event,
                "AUTOM. NOSTO": self._create_atm_withdrawal_event,
                "TILISIIRTO": self._create_bank_transfer_event,
                "VERKKOPANKKI": self._create_online_bank_event,
                "SEPA PIKA": self._create_mobile_pay_event
        }

        create_event = event_types.get(fragments[2])
        return create_event(date, name, amount, fragments[3])

    @staticmethod
    def _create_card_payment_event(date, name, amount, location):
        return Event.card_payment(date, name, amount, location)

    @staticmethod
    def _create_salary_event(date, name, amount, salary_label):
        return Event.salary(date, name, amount, salary_label)

    @staticmethod
    def _create_atm_withdrawal_event(date, name, amount, card_number):
        return Event.salary(date, name, amount, card_number)

    @staticmethod
    def _create_bank_transfer_event(date, name, amount, reference_number):
        return Event.salary(date, name, amount, reference_number)

    @staticmethod
    def _create_bank_transfer_event(date, name, amount, reference_number):
        return Event.salary(date, name, amount, reference_number)

    @staticmethod
    def _create_online_bank_event(date, name, amount, message):
        return Event.salary(date, name, amount, message)

    @staticmethod
    def _create_mobile_pay_event(date, name, amount, payment_number):
        return Event.salary(date, name, amount, payment_number)
