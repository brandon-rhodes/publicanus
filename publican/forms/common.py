from datetime import date, timedelta as Interval
from decimal import Decimal

two_places = Decimal('1.00')
zero = Decimal('0')

def cents(n):
    return n.quantize(two_places)


class Date(date):
    def next_business_day(self):
        w = self.weekday()
        if w < 6:
            return self
        return self + Interval(days=7 - w)

# These are here for forms to import, in case we swap in other classes later
Interval

class Filing(object):
    def __init__(self, form, period):
        self.form = form
        self.period = period
        self.pages = []

    def tally(self, company):
        self.form.tally(company, self)

    def new_page(self, number):
        p = Page(number)
        self.pages.append(p)
        return p

class Page(object):
    def __init__(self, number):
        self.number = number
