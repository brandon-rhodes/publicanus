"""Publican Middleware."""

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

        if request.user.is_authenticated():
            user = request.user
            cu = CompanyUser.objects.select_related('company').get(user=user)
            account = cu.company
            request.company = Company()
            request.company.account = account
            request.company.today = Date.today()
