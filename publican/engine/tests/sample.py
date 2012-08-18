"""Sample company that lives in RAM, not tied to the database or models."""

from datetime import datetime
from decimal import Decimal


class Account(object):
    def __init__(self, type):
        self.id = id(self)
        self.type = type


class Transaction(object):

    def __init__(self, date, debit_from, credit_to, amount, comment=''):
        self.id = id(self)
        self.date = date
        self.debit_from = debit_from
        self.credit_to = credit_to
        self.amount = amount
        self.comment = comment

    def __repr__(self):
        return '<Transaction ${}>'.format(self.amount)


def filter_transactions(transactions, **kw):
    tt = transactions
    period = kw.pop('within')
    if period:
        tt = (t for t in tt if period.start <= t.date <= period.end)
    debit_type = kw.pop('debit_type')
    if debit_type:
        tt = (t for t in tt if t.debit_from.type == debit_type)
    credit_type = kw.pop('credit_type')
    if credit_type:
        tt = (t for t in tt if t.credit_to.type == credit_type)
    return tt


T = Transaction

class Company(object):
    ein = '38-0218963'
    name = 'Crazy R Software'
    incorporation_date = datetime(2011, 8, 1)
    now = datetime(2012, 8, 20)

    business = Account('business')
    alice = Account('employee')
    bob = Account('employee')
    carol = Account('consultant')

    _transactions = [
        T(datetime(2011, 11, 29), business, alice, Decimal(10)),
        T(datetime(2011, 12, 29), business, alice, Decimal(10)),

        T(datetime(2012, 1, 29), business, alice, Decimal(2200)),
        T(datetime(2012, 1, 29), business, bob, Decimal(900)),
        T(datetime(2012, 1, 29), bob, business, Decimal(99)), # reimbursement
        T(datetime(2012, 2, 29), business, carol, Decimal(1000)),
        T(datetime(2012, 2, 29), business, alice, Decimal(2200)),
        T(datetime(2012, 3, 29), business, alice, Decimal(2200)),

        T(datetime(2012, 4, 29), business, alice, Decimal(10)),
       ]

    def transactions(self, **kw):
        return filter_transactions(self._transactions, **kw)


company = Company()
