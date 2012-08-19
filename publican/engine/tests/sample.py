"""Sample company that lives in RAM, not tied to the database or models."""

from decimal import Decimal

from publican.engine.company import Company
from publican.engine.filings import Filing
from publican.engine.kit import Date, Quarter, Year
from publican.engine.types import Account, Transaction
from publican.forms.registry import get_form


def build_company():
    """Create a sample `Company` with pre-loaded test data."""

    def make(cls, **kw):
        thing = cls()
        for k, v in kw.iteritems():
            setattr(thing, k, v)
        return thing

    def F(region, name, period, date):
        form = get_form(region, name)
        f = Filing(form, period)
        f.date = date
        return f

    b = Company(
        ein='38-0218963',
        name='Crazy R Software',
        incorporation_date=Date(2011, 8, 1)
        )

    b.today = Date(2012, 8, 20)  # override, so tests are predictable!

    business = make(Account, type='business')
    alice = make(Account, type='employee')
    bob = make(Account, type='employee')
    carol = make(Account, type='consultant')

    business.id, alice.id, bob.id, carol.id = range(4)

    b._filings = [
        F('us', '941', Quarter(2011, 3), Date(2011, 11, 5)),
        F('us', '940', Year(2011), Date(2012, 1, 20)),
        F('us', '941', Quarter(2011, 4), Date(2012, 1, 20)),
        F('us', '941', Quarter(2012, 1), Date(2012, 4, 15)),
        ]

    T = Transaction

    b._transactions = [
        make(T, date=Date(2011, 11, 29), debit_account=business,
             credit_account=alice, amount=Decimal(1400)),
        make(T, date=Date(2011, 12, 29), debit_account=business,
             credit_account=alice, amount=Decimal(2200)),

        make(T, date=Date(2012, 1, 29), debit_account=business,
             credit_account=alice, amount=Decimal(2200)),
        make(T, date=Date(2012, 1, 29), debit_account=business,
             credit_account=bob, amount=Decimal(900)),
        make(T, date=Date(2012, 1, 29), debit_account=bob,
             credit_account=business, amount=Decimal(99)), # reimbursement
        make(T, date=Date(2012, 2, 29), debit_account=business,
             credit_account=carol, amount=Decimal(1000)),
        make(T, date=Date(2012, 2, 29), debit_account=business,
             credit_account=alice, amount=Decimal(2200)),
        make(T, date=Date(2012, 3, 29), debit_account=business,
             credit_account=alice, amount=Decimal(2200)),

        make(T, date=Date(2012, 4, 29), debit_account=business,
             credit_account=alice, amount=Decimal(2200)),
        ]

    return b


company = build_company()
