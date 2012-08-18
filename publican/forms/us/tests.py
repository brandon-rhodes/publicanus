from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from publican.engine.time import Quarter
from . import irs_941


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
    incorporation_date = datetime(2011, 4, 1)
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


class Tests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company()

    def test_periods(self):
        self.assertEqual(
            [ period.name for period in irs_941.periods(self.company) ],
            ['2011-Q2', '2011-Q3', '2011-Q4', '2012-Q1', '2012-Q2', '2012-Q3']
            )

    def test_reckon(self):
        f = irs_941.reckon(self.company, Quarter(2012, 1))
        p = f.pages[0]
        self.assertEqual(p.line2, Decimal('7500.00'))
        self.assertEqual(p.line3, Decimal('896.25'))
        self.assertEqual(p.line5a2, Decimal('780.00'))
        self.assertEqual(p.line5c2, Decimal('217.50'))
        self.assertEqual(p.line14, Decimal('1893.75'))
