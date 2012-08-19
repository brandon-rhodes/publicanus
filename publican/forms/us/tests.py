from decimal import Decimal
from unittest import TestCase

from publican.engine.kit import Quarter, Year
from publican.engine.tests.sample import company
from ..registry import get_form


class Test940(TestCase):

    def test_periods(self):
        form = get_form('us', '940')
        self.assertEqual(
            [ period.name for period in form.periods(company) ],
            [u'2011', u'2012']
            )

    def test_reckon(self):
        form = get_form('us', '940')
        filings = form.tally(company, Year(2012))
        p = filings.pages[0]
        self.assertEqual(p.line3, Decimal('24000.00'))
        self.assertEqual(p.line6, Decimal('10000.00'))
        self.assertEqual(p.line14, Decimal('56.00'))


class Test941(TestCase):

    def test_periods(self):
        form = get_form('us', '941')
        self.assertEqual(
            [ period.name for period in form.periods(company) ],
            [u'2011-Q3', u'2011-Q4',
             u'2012-Q1', u'2012-Q2', u'2012-Q3', u'2012-Q4']
            )

    def test_reckon(self):
        form = get_form('us', '941')
        filing = form.tally(company, Quarter(2012, 1))
        p = filing.pages[0]
        self.assertEqual(p.line2, Decimal('10800.00'))
        self.assertEqual(p.line3, Decimal('1290.60'))
        self.assertEqual(p.line5a2, Decimal('1123.20'))
        self.assertEqual(p.line5c2, Decimal('313.20'))
        self.assertEqual(p.line14, Decimal('2727.00'))
