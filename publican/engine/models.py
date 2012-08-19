"""Database persistence for Publican.

"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
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
    filer = models.ForeignKey('Account', related_name='filings')
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
    """Our `Company` facade, backed by a Django database.

    See the parent `Company` class for more about the interface.

    One weakness of being backed by a real database is that it can get
    expensive to run the above filters many times per page; the front
    page, for example, needs to run .filings() twice for every month it
    displays!  Thanks to having separated our business logic out into a
    separate class, we have an easy solution: we offer complex pages the
    ability to pre-cache all of the data that first within the page's
    overall time period.  From that point on, all of their filtering is
    applied to the objects already cached in memory, instead of going
    out to hit the database again.

    """
    ein='38-0218963'
    name='Crazy R Software'
    incorporation_date=Date(2011, 8, 1)
    account = None
    today = None

    # Filters.

    def filings(self, form=None, period=None):
        """Implement the standard filings filter, as a Django query."""

        if self._filings is not None:
            return company.Company.filings(self, form=form, period=period)

        q = Q(filer=self.account)

        if form is not None:
            q &= Q(region=form.region, name=form.name)

        if period is not None:
            q &= Q(period=unicode(period))

        return list(Filing.objects.filter(q))

    def transactions(self, within=None, debit_type=None, credit_type=None):
        """Implement the standard transactions filter, as a Django query."""

        if self._transactions is not None:
            return company.Company.transactions(
                self, within=within, debit_type=debit_type,
                credit_type=credit_type)

        q = Q(debit_account=self.account) | Q(credit_account=self.account)

        if within is not None:
            period = within
            q &= Q(date__gte=period.start, date__lte=period.end)

        if debit_type is not None:
            q &= Q(debit_account__type=debit_type)

        if credit_type is not None:
            q &= Q(credit_account__type=credit_type)

        return list(Transaction.objects.filter(q).select_related(
            'debit_account', 'credit_account'))
