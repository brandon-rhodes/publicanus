"""Sample company that lives in RAM, not tied to the database or models."""

from datetime import date as Date
from decimal import Decimal

from publican.engine.filings import Filing
from publican.engine.kit import Quarter, Year
from publican.engine.types import Account
from publican.forms.registry import get_form


class SampleTransaction(object):
    def __init__(self, date, debit_from, credit_to, amount, comment=''):
        self.id = id(self)
        self.date = date
        self.debit_from = debit_from
        self.credit_to = credit_to
        self.amount = amount
        self.comment = comment

    def __repr__(self):
        return '<Transaction ${}>'.format(self.amount)


def filter_filings(filings, **kw):
    ff = filings

    form = kw.pop('form', None)
    if form is not None:
        # Forms are singletons, right?  Right.  (gulp!)
        ff = (f for f in ff if f.form is form)

    period = kw.pop('period', None)
    if period is not None:
        ff = (f for f in ff
              if f.period.start == period.start and f.period.end == period.end)

    return ff


def filter_transactions(transactions, **kw):
    tt = transactions

    period = kw.pop('within', None)
    if period is not None:
        tt = (t for t in tt if period.start <= t.date <= period.end)

    debit_type = kw.pop('debit_type', None)
    if debit_type is not None:
        tt = (t for t in tt if t.debit_from.type == debit_type)

    credit_type = kw.pop('credit_type', None)
    if credit_type is not None:
        tt = (t for t in tt if t.credit_to.type == credit_type)

    return tt


T = SampleTransaction

class Company(object):

    def F(region, name, period, date):
        form = get_form(region, name)
        f = Filing(form, period)
        f.date = date
        return f

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

    def filings(self, **kw):
        return filter_filings(self._filings, **kw)

    def transactions(self, **kw):
        return filter_transactions(self._transactions, **kw)


company = Company()
