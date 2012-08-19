from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response

from publican.engine.kit import Interval, Month, dollars, cents, get_period
#from publican.engine.tests.sample import company
from publican.forms import registry


class Row(object):
    """Throwaway class for the table rows we build for the template."""


@login_required
def index(request):
    company = _get_company(request)
    transactions = company.transactions
    filings_by_month = defaultdict(list)

    for form in sorted(registry.all_forms(), key=lambda f: f.name):
        for period in form.periods(company):
            filing = form.tally(company, period)
            filing.real_filings = list(company.filings(
                form=form,
                period=period,
                ))
            filing.state = (
                'filed' if filing.real_filings else
                'warn' if filing.due_date > company.today else
                'late'
                )
            display_month = _display_month(filing)
            filings_by_month[display_month].append(filing)

    sorted_months = sorted(filings_by_month.iterkeys())
    start = sorted_months[0]
    end = sorted_months[-1]
    now_month = company.today.replace(day=1)
    rows = []

    date = start
    while date <= end:
        month = Month(date.year, date.month)
        row = Row()
        row.date = date
        row.is_now = (date == now_month)
        row.employee_cost = dollars(sum(t.amount for t in transactions(
            within=month,
            debit_type='business',
            credit_type='employee',
            )))
        row.consultant_cost = dollars(sum(t.amount for t in transactions(
            within=month,
            debit_type='business',
            credit_type='consultant',
            )))
        row.filings = filings_by_month.get(date, ())
        row.total_due = cents(sum(f.balance_due for f in row.filings))
        rows.append(row)
        if date.month == 12:
            date = date.replace(year=date.year + 1, month=1)
        else:
            date = date.replace(month=date.month + 1)

    return render_to_response('publican/main.html', {
        'rows': rows,
        'this_month': company.today.replace(day=1),
        'today': company.today,
        })


@login_required
def filing(request, region, name, period_name):
    company = _get_company(request)
    form = registry.get_form(region, name)
    period = get_period(period_name, None)
    if form is None or period is None:
        raise Http404
    filing = form.tally(company, period)
    real_filings = sorted(company.filings(form=form, period=period),
                          key=lambda f: f.date)

    # How close to on-time was the initial filing?

    if real_filings:
        real_filings[0].offset = (filing.due_date - real_filings[0].date).days

    return render_to_response('publican/filing.html', {
        'filing': filing,
        'form': form,
        'grid': _generate_grid(filing),
        'real_filings': real_filings,
        'today': company.today,
        })


# Helpful functions.

def _get_company(request):
    """Return a `Company` facade for the current user's data."""
    from ..engine.models import CompanyUser, Company
    cu = CompanyUser.objects.get(user=request.user)
    print cu
    account = cu.company
    print account
    return Company(account)

def _display_month(filing):
    """Decide in which month we will display a given filing.

    Sometimes a form that one thinks of as "due at the end of July" is
    actually due on August 1st or 2nd because July 31st happens to fall
    on a weekend.  It would be unreasonable to display such a form in
    the interface as an "August" form, so we display such forms "early"
    by moving them back into the previous month.

    """
    return (filing.due_date - Interval(days=5)).replace(day=1)

def _generate_grid(filing):
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
