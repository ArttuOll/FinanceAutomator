from datetime import datetime
from ..model.event_extractor import EventExtractor
from ..model.event_calculator import EventCalculator

def write_report(save_dir, categories_tags):
    event_extractor = EventExtractor()
    events = event_extractor.events_from_file(save_dir)
    event_calculator = EventCalculator(events, categories_tags)

    values_by_category = event_calculator.calculate_values()

    datetime_now = datetime.now()
    report = f"Talousraportti {datetime_now}\n"

    for category, value in values_by_category.items():
        # TODO: liitä raporttimerkkijonoon
