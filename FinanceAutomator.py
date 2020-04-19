import json
from decimal import Decimal

from Classes import Event


def create_event(fragments):
    if fragments[2] == "KORTTIOSTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        location = fragments[3]
        card_event = Event.card_payment(date=date, name=name, amount=amount, location=location)

        return card_event

    elif fragments[2] == "PALKKA":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        salary_label = fragments[3]
        salary_event = Event.salary(date=date, name=name, amount=amount, salary_label=salary_label)

        return salary_event

    elif fragments[2] == "AUTOM. NOSTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        cardnumber = fragments[3]
        atm_event = Event.atm_withdrawal(date=date, name=name, amount=amount, cardnumber=cardnumber)

        return atm_event

    elif fragments[2] == "TILISIIRTO":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        refnumber = fragments[3]
        transfer_evet = Event.bank_transfer(date=date, name=name, amount=amount, refnumber=refnumber)

        return transfer_evet

    elif fragments[2] == "VERKKOPANKKI":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        message = fragments[3]
        online_event = Event.online_bank(date=date, name=name, amount=amount, message=message)

        return online_event

    elif fragments[2] == "SEPA PIKA":
        date = fragments[0]
        name = fragments[1]
        amount = fragments[4]
        payment_number = fragments[3]
        mobile_event = Event.mobilepay(date=date, name=name, amount=amount, payment_number=payment_number)

        return mobile_event


def clean_fragments(fragments_unclean):
    fragments = []
    for fragment in fragments_unclean:
        fragment = fragment.strip("\"")

        # Korvataan pilkut pisteillä
        if "," in fragment:
            fragment = fragment.replace(",", ".")

        fragments.append(fragment)

    return fragments


def sort_expenses(events):
    negative_events = []
    for event in events:
        if event.amount.startswith("-"):
            negative_events.append(event)
    return negative_events


def sort_incomes(events):
    positive_events = []
    for event in events:
        if not event.amount.startswith("-"):
            positive_events.append(event)
    return positive_events


def count_total(list):
    total = 0
    for value in list:
        total += Decimal(value.amount)
    return total


def count_expenses_by_tag(expenses, tag):
    global tags_object
    total = 0
    for expense in expenses:
        name = expense.name.lower()
        for keyword in tags_object[tag]:
            if keyword in name:
                total += Decimal(expense.amount)

    return total


def count_income_by_tag(incomes, tag):
    global tags_object
    total = 0
    for income in incomes:
        name = income.name.lower()
        for keyword in tags_object[tag]:
            if keyword in name:
                total += Decimal(income.amount)

    return total


def report():
    total_expense = count_total(expenses)
    total_income = count_total(incomes)
    balance = total_income + total_expense

    salary = count_income_by_tag(incomes, "salary")
    benefits = count_income_by_tag(incomes, "benefit")
    other_income = total_income - salary - benefits

    groceries = count_expenses_by_tag(expenses, "grocery")
    electricity = count_expenses_by_tag(expenses, "electricity")
    rent = count_expenses_by_tag(expenses, "rent")
    internet = count_expenses_by_tag(expenses, "internet")
    other_expenses = total_expense - groceries - rent - electricity

    print("Monthly report\n")

    print("Total income of the month:", total_income)
    print("Total expenses of the month:", total_expense)
    print("Balance:", balance)

    print("\nSources of income:")
    print("Salary:", salary)
    print("Benefits:", benefits)
    print("Other: ", other_income)

    print("\nExpenses on")
    print("Groceries:", groceries)
    print("Electricity:", electricity)
    print("Rent:", rent)
    print("Internet:", internet)
    print("Other: ", other_expenses)


with open("resources/tags", "r") as tags_file:
    data = tags_file.read()

    tags_object = json.loads(data)

print("Give filepath:")
filepath = input()

events = []
try:
    with open(filepath, "r", encoding="iso-8859-1") as transactions_file:
        all_lines = transactions_file.read().splitlines()
        # Delete header row
        lines = all_lines[1:]

        for line in lines:
            frags_unclean = line.split(";")

            frags = clean_fragments(frags_unclean)
            card_event = create_event(frags)
            events.append(card_event)

except FileNotFoundError:
    print("No such file!")

expenses = sort_expenses(events)
incomes = sort_incomes(events)

report()
