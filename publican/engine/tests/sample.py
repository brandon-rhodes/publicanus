"""Sample company that lives in RAM, not tied to the database or models."""

from decimal import Decimal

from publican.engine.company import Company
from publican.engine.filings import Filing
from publican.engine.kit import Date, Quarter, Year, months_range
from publican.engine.types import Account, Transaction


def build_sample(Account, Company, Filing, Transaction, assign_fake_ids=True):
    """Create a sample `Company` with pre-loaded test data."""

    def make(cls, **kw):
        thing = cls()
        for k, v in kw.iteritems():
            setattr(thing, k, v)
        return thing

    def F(filer, region, name, period, date):
        f = Filing()
        f.filer = filer
        f.region = region
        f.name = name
        f.period_name = period.name
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
        F(business, 'us', '941', Quarter(2011, 3), Date(2011, 11, 5)),
        F(business, 'us', '940', Year(2011), Date(2012, 1, 20)),
        F(business, 'us', '941', Quarter(2011, 4), Date(2012, 1, 20)),
        F(business, 'us', '941', Quarter(2012, 1), Date(2012, 4, 15)),
        ]

    c._transactions = []

    def add(**kw):
        c._transactions.append(make(Transaction, **kw))

    # Alice is the owner.

    for month in months_range(Date(2011, 11, 1), Date(2012, 8, 1)):
        add(date=month.end, debit_account=business,
            credit_account=alice, amount=Decimal(2000))

    # She had an employee for a few months.

    for month in months_range(Date(2011, 12, 1), Date(2012, 5, 1)):
        add(date=month.end, debit_account=business,
            credit_account=alice, amount=Decimal(1600))

    # And she has an active consultant.

    add(date=Date(2011, 12, 1), debit_account=business,
        credit_account=carol, amount=Decimal('572'))
    add(date=Date(2012, 1, 1), debit_account=business,
        credit_account=carol, amount=Decimal('983'))
    add(date=Date(2012, 2, 1), debit_account=business,
        credit_account=carol, amount=Decimal('1452'))
    add(date=Date(2012, 3, 1), debit_account=business,
        credit_account=carol, amount=Decimal('821'))
    add(date=Date(2012, 5, 1), debit_account=business,
        credit_account=carol, amount=Decimal('1396'))
    add(date=Date(2012, 6, 1), debit_account=business,
        credit_account=carol, amount=Decimal('1008'))
    add(date=Date(2012, 7, 1), debit_account=business,
        credit_account=carol, amount=Decimal('939'))

    return c


company = build_sample(Account, Company, Filing, Transaction)
