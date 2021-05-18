"""Määrittelee luokan EventExtractor ja sen käyttämät apufunktiot."""
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

    def extract_events_from_file(self, transactions_file):
        """Hoitaa tilitapahtumat sisältävän tiedoston lukemisen ja Event-olioita
        sisältävän listan palauttamisen."""

        try:
            return self.__read_events_from_file(transactions_file)
        except (IOError, TypeError) as error:
            print(f"Virhe yritettäessä lukea tilitapahtumia tiedostosta: {error}. Onko tilitapahtumatiedosto määritelty oikein?", file=stderr)
            return []

    def __read_events_from_file(self, file):
        events = []
        with open(file, "r", encoding="iso-8859-1") as events_file:
            all_lines = events_file.read().splitlines()

        # Delete header row
        lines = all_lines[1:]

        for line in lines:
            frags_unclean = line.split(";")
            frags = clean_fragments(frags_unclean)
            events.append(self.__create_event(frags))

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
    def _create_online_bank_event(date, name, amount, message):
        return Event.salary(date, name, amount, message)

    @staticmethod
    def _create_mobile_pay_event(date, name, amount, payment_number):
        return Event.salary(date, name, amount, payment_number)
