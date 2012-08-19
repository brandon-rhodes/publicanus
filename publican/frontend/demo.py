"""Present a welcome page and temporary account to Django Dash visitors!"""

import random
from string import ascii_lowercase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response

from publican.engine import models
from publican.engine.tests.sample import build_sample


def welcome_page(request):
    """For the purposes of this demo, offer one-click account creation."""

    url = request.GET.get('next', '/')
    return render_to_response('publican/login.html', {'url': url})


def goodbye_page(request):
    """Say goodbye."""

    if request.user.is_authenticated():
        logout(request)

    return render_to_response('publican/goodbye.html')


def create_demo(request):
    """Create a new company and user, and log the user into it."""

    name = ''.join(random.sample(ascii_lowercase, 8))
    pw = ''.join(random.sample(ascii_lowercase, 8))
    user = User.objects.create_user(name, 'demo@unknown.rhodesmill.org', pw)
    user.save()

    user = authenticate(username=name, password=pw)
    login(request, user)

    company = build_sample(models.Account, models.Company,
                           models.Filing, models.Transaction,
                           assign_fake_ids=False)

    company._accounts[0].save()

    company._accounts[1].save()
    models.NameAddress(
        account=company._accounts[1], name='Alice', address='123 Main, CA',
        ).save()

    company._accounts[2].save()
    models.NameAddress(
        account=company._accounts[1], name='Bob', address='37 Grove, OR',
        ).save()

    company._accounts[3].save()
    models.NameAddress(
        account=company._accounts[1], name='Carol', address='9110 W Bay, CA',
        ).save()

    for f in company._filings:
        f.filer = f.filer
        f.save()
    for t in company._transactions:
        t.credit_account = t.credit_account
        t.debit_account = t.debit_account
        t.save()

    cu = models.CompanyUser()
    cu.user = user
    cu.company = company.account
    cu.save()

    return redirect('/')
