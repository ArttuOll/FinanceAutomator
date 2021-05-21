from datetime import datetime

def get_current_month_tag():
    current_month = datetime.today().month
    if current_month == 1:
        return "Tammi"
    if current_month == 2:
        return "Helmi"
    if current_month == 3:
        return "Maalis"
    if current_month == 4:
        return "Huhti"
    if current_month == 5:
        return "Touko"
    if current_month == 6:
        return "Kesä"
    if current_month == 7:
        return "Heinä"
    if current_month == 8:
        return "Elo"
    if current_month == 9:
        return "Syys"
    if current_month == 10:
        return "Loka"
    if current_month == 11:
        return "Marras"
    if current_month == 12:
        return "Joulu"
