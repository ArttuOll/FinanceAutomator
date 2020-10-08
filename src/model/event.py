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
        """Luo Event-olion, joka kuvaa yhtä tilisiirtotapahtumaa."""

        event_type = "TILISIIRTO"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   refnumber=refnumber)

    @classmethod
    def card_payment(cls, date, name, amount, location):
        """Luo Event-olion, joka kuvaa yhtä korttimaksutapahtumaa."""

        event_type = "KORTTIOSTO"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   location=location)

    @classmethod
    def atm_withdrawal(cls, date, name, amount, cardnumber):
        """Luo Event-olion, joka kuvaa yhtä käteisnostotapahtumaa."""

        event_type = "AUTOM. NOSTO"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   cardnumber=cardnumber)

    @classmethod
    def online_bank(cls, date, name, amount, message):
        """Luo Event-olion, joka kuvaa yhtä verkkopankkimaksutapahtumaa."""

        event_type = "VERKKOPANKKI"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   message=message)

    @classmethod
    def salary(cls, date, name, amount, salary_label):
        """Luo Event-olion, joka kuvaa yhtä palkanmaksutapahtumaa."""

        event_type = "PALKKA"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   salary_label=salary_label)

    @classmethod
    def mobilepay(cls, date, name, amount, payment_number):
        """Luo Event-olion, joka kuvaa yhtä MobilePay-tapahtumaa."""

        event_type = "SEPA PIKA"
        return cls(date=date, name=name, amount=amount, event_type=event_type,
                   payment_number=payment_number)
