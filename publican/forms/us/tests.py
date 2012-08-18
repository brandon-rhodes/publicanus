from datetime import datetime
from unittest import TestCase
from . import irs_941

class Company(object):
    incorporation_date = datetime(2011, 4, 1)
    now = datetime(2012, 8, 20)

class Tests(TestCase):

    def test_one(self):
        company = Company()
        self.assertEqual(
            irs_941.periods(company),
            ['2011-Q2', '2011-Q3', '2011-Q4', '2012-Q1', '2012-Q2', '2012-Q3']
            )
