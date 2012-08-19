"""Database persistence for Publican.

"""
from django.contrib.auth.models import User
from django.db import models
from . import company
from . import types
from .kit import Date


class CompanyUser(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey('Account')


class Account(types.Account, models.Model):
    type = models.CharField(max_length=12)


class Transaction(types.Transaction, models.Model):
    date = models.DateField()
    debit_account = models.ForeignKey('Account', related_name='debits')
    credit_account = models.ForeignKey('Account', related_name='credits')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    comment = models.TextField(blank=True)

    def __init__(self, *args, **kw):
        models.Model.__init__(self, *args, **kw)


class Company(company.Company):
    ein='38-0218963'
    name='Crazy R Software'
    incorporation_date=Date(2011, 8, 1)

    def __init__(self, account):
        self.account = account
        self.today = Date.today()

    def transactions(self, **kwargs):
        # TODO
        return []

    def filings(self, **kwargs):
        # TODO
        return []
