from decimal import Decimal

two_places = Decimal('1.00')
zero = Decimal('0')

def cents(n):
    return n.quantize(two_places)


class Filing(object):
    def __init__(self, period):
        self.period = period
        self.pages = []

    def new_page(self, number):
        p = Page(number)
        self.pages.append(p)
        return p


class Page(object):
    def __init__(self, number):
        self.number = number
