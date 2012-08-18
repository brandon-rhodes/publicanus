from calendar import mdays
from datetime import date as Date, timedelta

one_day = timedelta(days=1)

class Period(object):
    name = None
    start = None
    end = None

class Year(Period):
    def __init__(self, number):
        self.number = number
        self.start = Date(number, 1, 1)
        self.end = Date(number, 12, 31)

    def __unicode__(self):
        return u'{}'.format(self.year)

    def next(self):
        return Year(self.number + 1)

class Quarter(Period):
    def __init__(self, year, number):
        self.year = year
        self.number = number

        month = number * 3
        self.start = Date(year, month - 2, 1)
        self.end = Date(year, month, mdays[month])  # works: month != Feb

    def __unicode__(self):
        return u'{}-Q{}'.format(self.year, self.number)

    def next(self):
        if self.number == 4:
            return Quarter(self.year + 1, 1)
        return Quarter(self.year, self.number + 1)

def years_range(start, end):
    number = start.year
    year = Year(number)
    yield year
    while year.end < end:
        year = year.next()
        yield year

def quarters_range(start, end):
    year = start.year
    number = (start.month + 2) // 3
    quarter = Quarter(year, number)
    yield quarter
    while quarter.end < end:
        quarter = quarter.next()
        yield quarter
