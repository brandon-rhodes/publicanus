from collections import defaultdict

from django.http import Http404
from django.shortcuts import render_to_response

from publican.engine.kit import Interval, cents, get_period
from publican.engine.tests.sample import company
from publican.forms import registry
from publican.forms.common import Filing


class Row(object):
    """Throwaway class for the table rows we build for the template."""


def index(request):

    months = defaultdict(list)

    for form in sorted(registry.all_forms(), key=lambda f: f.name):
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


def filing(request, region, name, period_name):
    forms = [ f for f in registry.forms_for(region) if f.name == name ]
    period = get_period(period_name, None)
    if len(forms) != 1 or period is None:
        raise Http404
    form = forms[0]
    filing = Filing(form, period)
    filing.tally(company)
    return render_to_response('publican/filing.html', {
        'filing': filing,
        'form': form,
        'grid': generate_grid(filing),
        })

# Helpful functions.

def _display_month(filing):
    """Decide in which month we will display a given filing.

    Sometimes a form that one thinks of a "due at the end of July" is
    actually due on August 1st or 2nd because July 31st happens to fall
    on a weekend.  It would be unreasonable to display such a form in
    the interface as an "August" form, so we display such forms "early"
    by moving them back into the previous month.

    """
    return (filing.due_date - Interval(days=5)).replace(day=1)

def generate_grid(filing):
    """Convert a form's `grid` string into a table structure.

    This logic is tightly coupled with the for loops that it feeds,
    which live inside of the template that renders the filing page.

    """
    def generate_row(page, line):
        for spec in line.split():
            attr = spec.strip('-')
            if attr.startswith('line'):
                name = attr[4:]         # 'line5b' becomes '5b.'
            elif attr == 'x':
                name = ''               # use 'x' for empty grid cells
            else:
                name = attr.capitalize()
            hyphens = len(spec) - len(attr)  # for 'foo--' this is 2
            colspan = 2 * hyphens + 1 if hyphens else None
            if attr == 'x':
                datum = u''
            else:
                datum = getattr(page, attr, u'?')
            yield name, datum, colspan

    for page in filing.pages:
        grid = filing.form.grids[page.number]
        for line in grid.splitlines():
            if not line.strip():
                continue
            yield generate_row(page, line)
