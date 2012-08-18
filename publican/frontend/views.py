from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response

from publican.engine.tests.sample import company
from publican.forms.registry import all_forms

def _due_month(pair):
    d = pair[1].due_date
    return datetime(d.year, d.month + (1 if d.day < 6 else 0), 1)

def index(request):
    forms = all_forms()
    seq = []
    for form in forms:
        for period in form.periods(company):
            filing = form.reckon(company, period)
            seq.append((form, filing))
    seq.sort(key=_due_month)
    return render_to_response('publican/main.html', {
            'seq': groupby(seq),
            })
