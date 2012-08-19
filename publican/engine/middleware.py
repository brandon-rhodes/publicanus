"""Publican Middleware."""

from django.core.exceptions import ObjectDoesNotExist

from .kit import Date
from .models import CompanyUser, Company

class CompanyMiddleware(object):

    def process_request(self, request):
        """Install a `Company` facade for the current user's data."""

        request.company = None

        # Developers: switch this to "True" to test against a mockup in RAM.

        if False:
            from publican.engine.tests.sample import company
            request.company = company
            return

        # Find the Account object that represents this user business.

        if not request.user.is_authenticated():
            return

        user = request.user
        try:
            cu = CompanyUser.objects.select_related('company').get(user=user)
        except ObjectDoesNotExist:
            return

        account = cu.company

        # Build our Facade and store it on `request`.

        request.company = Company()
        request.company.account = account
        request.company.today = Date.today()
