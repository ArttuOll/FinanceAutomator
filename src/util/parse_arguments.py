"""Määrittelee funktion parse_arguments ja sen riippuvuudet"""
from argparse import ArgumentParser

def parse_arguments():
    """Lukee käyttäjän syötteestä tämän syöttämät argumentit ja palauttaa ne
    NameSpace-oliossa, jossa argumenttien pitkät nimet ovat sen oliomuuttujina"""
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
            "-g", "--guided", action="store_true", help="Suorita ohjattu asetustiedoston luonti")
    argument_parser.add_argument(
            "-p", "--print", action="store_true", help="""Tulosta komennon ulostulo""")

    subparsers = argument_parser.add_subparsers(dest="report",
            help="""Tuota raportti kuluistasi haluamallasi aikavälillä.""")

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("-s", "--start", type=str, default="", help="""Aloituspäivämäärä""")
    report_parser.add_argument( "-e", "--end", type=str, default="", help="""Lopetuspäivämäärä""",)

    return argument_parser.parse_args()
