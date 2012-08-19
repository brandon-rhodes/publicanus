"""Database persistence for Publican.

"""
from django.contrib.auth.models import User
from django.db import models
from . import types


class CompanyUser(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey('Account')


class Account(types.Account, models.Model):
    type = models.CharField(max_length=12)
