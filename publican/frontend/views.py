from django.shortcuts import render_to_response

from publican.engine.tests.sample import company
from publican.forms.registry import all_forms

def index(request):
    forms = all_forms()
    seq = []
    for form in forms:
        for period in form.periods(company):
            filing = form.reckon(company, period)
            seq.append((period, form, filing))
    return render_to_response('publican/main.html', {
            'seq': seq,
            })
