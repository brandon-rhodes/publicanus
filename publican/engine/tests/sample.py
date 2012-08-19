"""Sample company that lives in RAM, not tied to the database or models."""

from decimal import Decimal

from publican.engine.company import Company
from publican.engine.filings import Filing
from publican.engine.kit import Date, Quarter, Year
from publican.engine.types import Account, Transaction
from publican.forms.registry import get_form


def build_sample(Account, Company, Filing, Transaction, assign_fake_ids=True):
    """Create a sample `Company` with pre-loaded test data."""

    def make(cls, **kw):
        thing = cls()
        for k, v in kw.iteritems():
            setattr(thing, k, v)
        return thing

    def F(region, name, period, date):
        form = get_form(region, name)
        f = Filing()
        f.region = region
        f.name = name
        f.form = form
        f.period = period
        f.date = date
        return f

    c = Company()
    c.ein = '38-0218963',
    c.name = 'Crazy R Software',
    c.incorporation_date = Date(2011, 8, 1)

    c.today = Date(2012, 8, 20)  # override, so tests are predictable!

    alice = make(Account, type='employee')
    bob = make(Account, type='employee')
    carol = make(Account, type='consultant')

    business = c.account
    if business is None:
        business = make(Account, type='business')
        c.account = business

    if assign_fake_ids:
        business.id, alice.id, bob.id, carol.id = range(4)

    c._accounts = [business, alice, bob, carol]

    c._filings = [
        F('us', '941', Quarter(2011, 3), Date(2011, 11, 5)),
        F('us', '940', Year(2011), Date(2012, 1, 20)),
        F('us', '941', Quarter(2011, 4), Date(2012, 1, 20)),
        F('us', '941', Quarter(2012, 1), Date(2012, 4, 15)),
        ]

    T = Transaction

    c._transactions = [
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

    return c


company = build_sample(Account, Company, Filing, Transaction)
