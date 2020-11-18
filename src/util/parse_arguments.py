"""Määrittelee funktion parse_arguments ja sen riippuvuudet"""
from argparse import ArgumentParser

def parse_arguments():
    """Lukee käyttäjän syötteestä tämän syöttämät argumentit ja palauttaa ne
    NameSpace-oliossa, jossa argumenttien pitkät nimet ovat sen oliomuuttujina"""
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
            "-g", "--guided", action="store_true", help="Suorita ohjattu asetustiedoston luonti")
    argument_parser.add_argument(
            "-r", "--report", action="store_true",
            help="""Kirjoittaa raportin viime kuukauden tilitapahtumista
                 tallennuskansiossa sijaitsevaan raporttitiedostoon.""")
    argument_parser.add_argument(
            "-p", "--print", action="store_true", help="""Tulosta komennon ulostulo""")

    return argument_parser.parse_args()
