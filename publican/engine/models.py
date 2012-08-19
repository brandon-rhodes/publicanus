"""Database persistence for Publican.

"""
from django.contrib.auth.models import User
from django.db import models
from . import company
from . import filings
from . import types
from .kit import Date

# Associate each Django user with a company that they manage.

class CompanyUser(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey('Account')

# Persistent versions of each of our objects.

class Account(types.Account, models.Model):
    type = models.CharField(max_length=12)


class Filing(filings.Filing, models.Model):
    region = models.CharField(max_length=12)
    name = models.CharField(max_length=12)
    period = models.CharField(max_length=12)
    date = models.DateField()


class Transaction(types.Transaction, models.Model):
    date = models.DateField()
    debit_account = models.ForeignKey('Account', related_name='debits')
    credit_account = models.ForeignKey('Account', related_name='credits')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    comment = models.TextField(blank=True)


class Company(company.Company):
    ein='38-0218963'
    name='Crazy R Software'
    incorporation_date=Date(2011, 8, 1)
    account = None
    today = None

    def filings(self, form=None, period=None):
        """Implement the standard transactions filter, as a Django query."""
        q = Filing.objects

        if form is not None:
            q = q.filter(region=form.region, name=form.name)

        if period is not None:
            q = q.filter(period=unicode(period))

        return q.all()

    def transactions(self, **kwargs):
        # TODO
        return []
