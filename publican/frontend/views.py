from collections import defaultdict
from datetime import datetime

from django.shortcuts import render_to_response

from publican.engine.kit import cents
from publican.engine.tests.sample import company
from publican.forms.common import Filing
from publican.forms.registry import all_forms


class Row(object):
    """Throwaway class for the table rows we build for the template."""


def _display_month(filing):
    d = filing.due_date
    return datetime(d.year, d.month + (1 if d.day < 6 else 0), 1)


def index(request):

    months = defaultdict(list)

    for form in sorted(all_forms(), key=lambda f: f.name):
        for period in form.periods(company):
            filing = Filing(form, period)
            filing.tally(company)
            display_month = _display_month(filing)
            months[display_month].append(filing)

    rows = []

    for month, filings in sorted(months.iteritems()):
        row = Row()
        row.month = month
        row.filings = filings
        row.total_due = cents(sum(f.balance_due for f in filings))
        rows.append(row)

    return render_to_response('publican/main.html', {
        'rows': rows,
        })


def filing(request, region, name, period):
    return render_to_response('publican/filing.html', {
        })
