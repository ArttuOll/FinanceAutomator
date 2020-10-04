from decimal import Decimal

class Event:
    """Kuvaa yhtä tilitapahtumaa. Sisältää tilitapahtuman ominaisuudet. 
    Muokattava vastaamaan käyttäjän pankin tarjoaman tilitapahtumatiedoston 
    kenttiä."""

    def __init__(self, date: str, name: str, amount: str, event_type=None, 
                 location=None, refnumber=None, cardnumber=None, message=None, 
                 salary_label=None, payment_number=None):
        self.date = date
        self.name = name
        self.amount = Decimal(amount)
        self.event_type = event_type
        self.location = location
        self.refnumber = refnumber
        self.cardnumber = cardnumber
        self.message = message
        self.salary_label = salary_label
        self.payment_number = payment_number

    @classmethod
    def bank_transfer(cls, date, name, amount, refnumber):
        date = date
        name = name
        amount = amount
        event_type = "TILISIIRTO"
        refnumber = refnumber
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   refnumber=refnumber)

    @classmethod
    def card_payment(cls, date, name, amount, location):
        date = date
        name = name
        amount = amount
        event_type = "KORTTIOSTO"
        location = location
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   location=location)

    @classmethod
    def atm_withdrawal(cls, date, name, amount, cardnumber):
        date = date
        name = name
        amount = amount
        event_type = "AUTOM. NOSTO"
        cardnumber = cardnumber
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   cardnumber=cardnumber)

    @classmethod
    def online_bank(cls, date, name, amount, message):
        date = date
        name = name
        amount = amount
        event_type = "VERKKOPANKKI"
        message = message
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   message=message)

    @classmethod
    def salary(cls, date, name, amount, salary_label):
        date = date
        name = name
        amount = amount
        event_type = "PALKKA"
        salary_label = salary_label
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   salary_label=salary_label)

    @classmethod
    def mobilepay(cls, date, name, amount, payment_number):
        date = date
        name = name
        amount = amount
        event_type = "SEPA PIKA"
        payment_number = payment_number
        return cls(date=date, name=name, amount=amount, event_type=event_type, 
                   payment_number=payment_number)


