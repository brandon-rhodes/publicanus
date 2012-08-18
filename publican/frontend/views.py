from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response

from publican.engine.tests.sample import company
from publican.forms.common import Filing
from publican.forms.registry import all_forms

def _display_month(filing):
    d = filing.due_date
    return datetime(d.year, d.month + (1 if d.day < 6 else 0), 1)

def index(request):

    seq = []
    for form in all_forms():
        for period in form.periods(company):
            filing = Filing(form, period)
            filing.tally(company)
            filing.display_month = _display_month(filing)
            seq.append(filing)

    seq.sort(key=lambda f: f.form.name)
    seq.sort(key=lambda f: f.display_month)

    seq = [(k, list(v)) for k, v in groupby(seq, lambda f: f.display_month)]

    return render_to_response('publican/main.html', {
            'seq': seq
            })
