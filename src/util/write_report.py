"""Määrittelee funktion write_report ja sen riippuvuudet"""
import json
from datetime import datetime
from ..model.event_extractor import EventExtractor
from ..model.event_calculator import EventCalculator

def write_report(save_dir, transactions_dir, categories_tags, print_output=False):
    event_extractor = EventExtractor()
    events = event_extractor.events_from_file(transactions_dir)
    event_calculator = EventCalculator(events, categories_tags)

    values_by_category = event_calculator.calculate_values()

    datetime_now = datetime.now()
    report = f"Talousraportti {datetime_now}\n"

    for category, value in values_by_category.items():
        report += f"{category}: {value}\n"

    if print_output:
        print(report)
