from decimal import Decimal

two_places = Decimal('1.00')
zero = Decimal('0')

def cents(n):
    return n.quantize(two_places)


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
