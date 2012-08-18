from calendar import mdays
from datetime import datetime, timedelta

one_day = timedelta(days=1)

class Period(object):
    name = None
    start = None
    end = None

class Quarter(Period):
    def __init__(self, year, number):
        self.year = year
        self.number = number

        month = number * 3
        self.start = datetime(year, month - 2, 1)
        self.end = datetime(year, month, mdays[month])  # works: month != Feb

    def __unicode__(self):
        return u'{}-Q{}'.format(self.year, self.number)

    def next(self):
        if self.number == 4:
            return Quarter(self.year + 1, 1)
        return Quarter(self.year, self.number + 1)

def quarters_range(start, end):
    year = start.year
    number = (start.month + 2) // 3
    quarter = Quarter(year, number)
    yield quarter
    while quarter.end < end:
        quarter = quarter.next()
        yield quarter
