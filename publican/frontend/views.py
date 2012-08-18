from django.shortcuts import render_to_response

from publican.engine.tests.sample import company
from publican.forms.registry import all_forms

def index(request):
    forms = all_forms()
    for form in forms:
        periods = form.periods(company)
        filings = [form.reckon(company, period) for period in periods]
        print filings
    return render_to_response('publican/main.html', {
            'filings': filings,
            })
