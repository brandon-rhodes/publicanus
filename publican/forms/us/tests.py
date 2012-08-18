from decimal import Decimal
from unittest import TestCase

from publican.engine.tests.sample import company
from publican.engine.time import Quarter
from . import irs_941

class Test941(TestCase):

    def test_periods(self):
        self.assertEqual(
            [ period.name for period in irs_941.periods(company) ],
            ['2011-Q2', '2011-Q3', '2011-Q4', '2012-Q1', '2012-Q2', '2012-Q3']
            )

    def test_reckon(self):
        f = irs_941.reckon(company, Quarter(2012, 1))
        p = f.pages[0]
        self.assertEqual(p.line2, Decimal('7500.00'))
        self.assertEqual(p.line3, Decimal('896.25'))
        self.assertEqual(p.line5a2, Decimal('780.00'))
        self.assertEqual(p.line5c2, Decimal('217.50'))
        self.assertEqual(p.line14, Decimal('1893.75'))
