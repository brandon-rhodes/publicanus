from decimal import Decimal

from publican.engine.time import quarters_range
from ..common import Filing, cents, zero

arbitrary = Decimal('0.1195')
point104 = Decimal('.104')
point029 = Decimal('.029')


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
    p.line3 = cents(wages * arbitrary)            # TODO

    p.line5a1 = wages                             # TODO
    p.line5b1 = 0                                 # TODO
    p.line5c1 = wages                             # TODO

    p.line5a2 = cents(p.line5a1 * point104)
    p.line5b2 = cents(p.line5b1 * point104)
    p.line5c2 = cents(p.line5c1 * point029)

    p.line5d = p.line5a2 + p.line5b2 + p.line5c2
    p.line5e = zero

    p.line6e = p.line3 + p.line5d + p.line5e

    p.line10 = p.line6e

    p.line14 = p.line10

    # TODO: page 2

    filing.due = p.line14

    return filing
