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


print("Give file path:")

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

income = 0
expenses = 0
for event in events:
    if event.amount.startswith("-"):
        expenses -= round(float(event.amount))
    else:
        income += round(float(event.amount))

print("Tulot", income, "Kulut", expenses)
