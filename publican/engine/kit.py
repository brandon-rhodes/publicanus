"""Helpful constants, functions, and classes for use of the Publican."""

from calendar import isleap, mdays
from datetime import date, timedelta
from decimal import Decimal

# Conveniences when working with decimals.

zero = Decimal('0.00')
zero_places = Decimal('1')
two_places = Decimal('1.00')

def dollars(n):
    return (n or zero).quantize(zero_places)

def cents(n):
    return (n or zero).quantize(two_places)

# Supercharged versions of the date and timedelta, that have the
# additional advantage that they are capitalized and so stop getting
# confused with my variables.  (I use "date" a lot.)

class Date(date):
    def next_business_day(self):
        w = self.weekday()
        if w < 6:
            return self
        return self + Interval(days=7 - w)

class Interval(timedelta):
    pass

# Periods of time have both a beginning and an end.

class Period(object):
    name = None

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

class Year(Period):
    def __init__(self, number):
        self.number = number
        self.start = Date(number, 1, 1)
        self.end = Date(number, 12, 31)

    def __unicode__(self):
        return u'{}'.format(self.number)

    def next(self):
        return Year(self.number + 1)

class Month(Period):
    def __init__(self, year, number):
        self.year = year
        self.number = number
        self.start = Date(year, number, 1)
        bump = (number == 2) and isleap(year)
        self.end = Date(year, number, mdays[number] + bump)

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

# Routines for working with Periods.

_die = object()

def get_period(name, default=_die):
    """Return the period with the given name."""
    a = str(name).split('-')

    if len(a) == 2:
        year = int(a[0])
        if a[1].startswith('Q'):
            number = int(a[1][1:])
            return Quarter(year, number)
        else:
            return Month(year, int(a[1]))
    elif len(a) == 1:
        year = int(a[0])
        return Year(year)

    if default is not _die:
        return default

    raise ValueError('there is no Period named {!r}'.format(name))

def years_range(start, end):
    """Return the years from date `start` to `end` inclusive."""
    number = start.year
    year = Year(number)
    yield year
    while year.end < end:
        year = year.next()
        yield year

def quarters_range(start, end):
    """Return the quarters from date `start` to `end` inclusive."""
    year = start.year
    number = (start.month + 2) // 3
    quarter = Quarter(year, number)
    yield quarter
    while quarter.end < end:
        quarter = quarter.next()
        yield quarter
