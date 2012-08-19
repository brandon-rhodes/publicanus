"""Sample company that lives in RAM, not tied to the database or models."""

from datetime import date as Date
from decimal import Decimal

from publican.engine.business import Business
from publican.engine.filings import Filing
from publican.engine.kit import Quarter, Year
from publican.engine.types import Account, Transaction
from publican.forms.registry import get_form


class Company(Business):
    """A sample `Business` with pre-loaded test data."""

    def F(region, name, period, date):
        form = get_form(region, name)
        f = Filing(form, period)
        f.date = date
        return f

    T = Transaction

    ein = '38-0218963'
    name = 'Crazy R Software'
    incorporation_date = Date(2011, 8, 1)
    today = Date(2012, 8, 20)

    business = Account('business')
    alice = Account('employee')
    bob = Account('employee')
    carol = Account('consultant')

    _filings = [
        F('us', '941', Quarter(2011, 3), Date(2011, 11, 5)),
        F('us', '940', Year(2011), Date(2011, 1, 20)),
        F('us', '941', Quarter(2011, 4), Date(2011, 1, 20)),
        F('us', '941', Quarter(2012, 1), Date(2011, 4, 15)),
        ]

    _transactions = [
        T(Date(2011, 11, 29), business, alice, Decimal(1400)),
        T(Date(2011, 12, 29), business, alice, Decimal(2200)),

        T(Date(2012, 1, 29), business, alice, Decimal(2200)),
        T(Date(2012, 1, 29), business, bob, Decimal(900)),
        T(Date(2012, 1, 29), bob, business, Decimal(99)), # reimbursement
        T(Date(2012, 2, 29), business, carol, Decimal(1000)),
        T(Date(2012, 2, 29), business, alice, Decimal(2200)),
        T(Date(2012, 3, 29), business, alice, Decimal(2200)),

        T(Date(2012, 4, 29), business, alice, Decimal(2200)),
        ]

    del F, T

company = Company()
