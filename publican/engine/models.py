"""Database persistence for Publican.

"""
from django.db import models
from . import types

class Account(models.Model, types.Account):
    type = models.CharField(max_length=12)
