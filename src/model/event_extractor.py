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

        if fragments[2] == "KORTTIOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            location = fragments[3]

            return Event.card_payment(date=date, name=name, amount=amount, location=location)

        elif fragments[2] == "PALKKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            salary_label = fragments[3]

            return Event.salary(date=date, name=name, amount=amount, salary_label=salary_label)

        elif fragments[2] == "AUTOM. NOSTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            cardnumber = fragments[3]

            return Event.atm_withdrawal(date=date, name=name, amount=amount, cardnumber=cardnumber)

        elif fragments[2] == "TILISIIRTO":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            refnumber = fragments[3]

            return Event.bank_transfer(date=date, name=name, amount=amount, refnumber=refnumber)

        elif fragments[2] == "VERKKOPANKKI":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            message = fragments[3]

            return Event.online_bank(date=date, name=name, amount=amount, message=message)

        elif fragments[2] == "SEPA PIKA":
            date = fragments[0]
            name = fragments[1]
            amount = fragments[4]
            payment_number = fragments[3]

            return Event.mobilepay(date=date, name=name, amount=amount,
                                   payment_number=payment_number)

        else:
            return None
