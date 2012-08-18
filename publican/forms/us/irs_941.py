from calendar import mdays
from datetime import datetime, timedelta
from decimal import Decimal

from publican.engine.time import quarters_range
from ..common import Filing, cents, zero

_arbitrary = Decimal('0.1195')
_point104 = Decimal('.104')
_point029 = Decimal('.029')


name = u"941"
title = u"Employer's QUARTERLY Federal Tax Return"


def periods(company):
    return list(quarters_range(company.incorporation_date, company.now))


def reckon(company, period):
    tlist = list(company.transactions(
        within=period,
        debit_type='business',
        credit_type='employee',
        ))
    number_of_employees = len(set(t.credit_to.id for t in tlist))
    wages = sum(t.amount for t in tlist)

    filing = Filing(period)
    p = filing.new_page(1)

    p.ein = company.ein
    p.name = company.name

    p.quarter1 = 'X' if period.number == 1 else ''
    p.quarter2 = 'X' if period.number == 2 else ''
    p.quarter3 = 'X' if period.number == 3 else ''
    p.quarter4 = 'X' if period.number == 4 else ''

    p.line1 = number_of_employees
    p.line2 = wages
    p.line3 = cents(wages * _arbitrary)           # TODO

    p.line5a1 = wages                             # TODO
    p.line5b1 = 0                                 # TODO
    p.line5c1 = wages                             # TODO

    p.line5a2 = cents(p.line5a1 * _point104)
    p.line5b2 = cents(p.line5b1 * _point104)
    p.line5c2 = cents(p.line5c1 * _point029)

    p.line5d = p.line5a2 + p.line5b2 + p.line5c2
    p.line5e = zero

    p.line6e = p.line3 + p.line5d + p.line5e

    p.line10 = p.line6e

    p.line14 = p.line10

    # TODO: page 2

    filing.balance_due = p.line14

    y = period.end.year
    m = period.end.month
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    filing.due_date = datetime(y, m, mdays[m])
    while filing.due_date.weekday() > 4:
        filing.due_date += timedelta(days=1)

    return filing
