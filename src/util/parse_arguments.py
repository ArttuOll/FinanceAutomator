"""Määrittelee funktion parse_arguments ja sen riippuvuudet"""

from argparse import ArgumentParser

from .write_report import write_analytical_report, write_report


def parse_arguments():
    """Lukee käyttäjän syötteestä tämän syöttämät argumentit ja palauttaa ne
    NameSpace-oliossa, jossa argumenttien pitkät nimet ovat sen oliomuuttujina"""
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
            "-g", "--guided", action="store_true", help="Suorita ohjattu asetustiedoston luonti")
    argument_parser.add_argument(
            "-p", "--print_output", action="store_true", help="""Tulosta komennon ulostulo""")

    _handle_subcommands(argument_parser)

    return argument_parser.parse_args()


def _handle_subcommands(argument_parser):
    subparsers = argument_parser.add_subparsers(title="Alikomennot")
    report_parser = subparsers.add_parser("report")
    report_parser.set_defaults(func=_handle_report_commands)

    _handle_report_operation_subcommands(report_parser)


def _handle_report_operation_subcommands(report_parser):
    operation_parsers = report_parser.add_subparsers(dest="operation", help="""Käytä näitä
            komentoja raporttien käsittelyyn haluamallasi tavalla""")

    sum_parser = operation_parsers.add_parser("sum")
    sum_parser.add_argument("-s", "--start", type=str, default="", help="""Aloituspäivämäärä""")
    sum_parser.add_argument( "-e", "--end", type=str, default="", help="""Lopetuspäivämäärä""",)
    sum_parser.set_defaults(func=_handle_operation_commands)


def _handle_report_commands(configs_object, args):
    locations = {
            "save" : configs_object["save_dir"],
            "transactions": configs_object["transactions_dir"]
            }

    categories_tags = configs_object["categories_tags"]
    write_report(locations, categories_tags, print_output=args.print_output)


def _handle_operation_commands(configs, args):
    operation = args.operation
    write_analytical_report(operation, args.start, configs["save_dir"],
        print_output=args.print_output, end_date=args.end)
