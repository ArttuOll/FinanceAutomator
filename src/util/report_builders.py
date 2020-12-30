"""Määrittelee raporttien merkkijonomuotoiluun käytettävät funktiot"""

def build_human_readable_report(timestamp, values_by_category, title):
    """Muotoilee ihmisluettavan raportin annettujen otsakkeen, raportin kategoriakohtaisten arvojen
    ja aikaleiman perusteella ja palauttaa tuloksen merkkijonona"""

    title = f"\n{title}\n" if title not in "" else f"\nTalousraportti {timestamp}\n"
    report = title
    for category, value in values_by_category.items():
        report += f"{category}: {value}\n"

    return report

def build_machine_readable_report(timestamp, values_by_category):
    """Muotoilee koneluettavan raportin annettujen otsakkeen, raportin kategoriakohtaisten arvojen
    ja aikaleiman perusteella ja palauttaa tuloksen merkkijonona"""
    report_dict = values_by_category
    report_dict["timestamp"] = timestamp
    return report_dict
