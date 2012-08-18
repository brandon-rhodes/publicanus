from decimal import Decimal
from unittest import TestCase

from publican.engine.kit import Quarter, Year
from publican.engine.tests.sample import company
from .. common import Filing
from . import form_940, form_941


class Test940(TestCase):

    def test_periods(self):
        self.assertEqual(
            [ unicode(period) for period in form_940.periods(company) ],
            [u'2011', u'2012']
            )

    def test_reckon(self):
        f = Filing(form_940, Year(2012))
        f.tally(company)
        p = f.pages[0]
        self.assertEqual(p.line3, Decimal('9700.00'))
        self.assertEqual(p.line6, Decimal('1800.00'))
        self.assertEqual(p.line14, Decimal('56.00'))


class Test941(TestCase):

    def test_periods(self):
        self.assertEqual(
            [ unicode(period) for period in form_941.periods(company) ],
            [u'2011-Q3', u'2011-Q4',
             u'2012-Q1', u'2012-Q2', u'2012-Q3', u'2012-Q4']
            )

    def test_reckon(self):
        f = Filing(form_941, Quarter(2012, 1))
        f.tally(company)
        p = f.pages[0]
        self.assertEqual(p.line2, Decimal('7500.00'))
        self.assertEqual(p.line3, Decimal('896.25'))
        self.assertEqual(p.line5a2, Decimal('780.00'))
        self.assertEqual(p.line5c2, Decimal('217.50'))
        self.assertEqual(p.line14, Decimal('1893.75'))
