from decimal import Decimal
from itertools import groupby

from publican.engine.time import years_range
from ..common import Date, zero

name = u"940"
title = u"Employer's Annual Federal Unemployment (FUTA) Tax Return"


_sevenk = Decimal('7000.00')
_eighthpercent = Decimal('.008')
_sixthpercent = Decimal('.006')


def periods(company):
    return list(years_range(company.incorporation_date, company.now))


def tally(company, filing):
    period = filing.period

    tlist = list(company.transactions(
        within=period,
        debit_type='business',
        credit_type='employee',
        ))
    wages = sum(t.amount for t in tlist)

    p = filing.new_page(1)

    p.ein = company.ein
    p.name = company.name

    p.line3 = wages

    get_employee_id = lambda t: t.account.id
    tlist.sort(key=get_employee_id)
    p.line5 = sum(t.amount - _sevenk
                  for k, sublist in groupby(tlist, get_employee_id)
                  for t in sublist)

    p.line6 = p.line5
    p.line7a = p.line3 - p.line6

    p.line7b = _sevenk  # TODO
    p.line7d = zero     # TODO

    p.line7c = p.line7b * _eighthpercent
    p.line7e = p.line7d * _sixthpercent

    p.line8 = p.line7c + p.line7e
    p.line11 = zero     # TODO
    p.line12 = p.line8 + p.line11
    p.line14 = p.line12

    # TODO: page 2

    filing.balance_due = p.line14
    filing.due_date = Date(period.end.year + 1, 1, 31).next_business_day()

    return filing
