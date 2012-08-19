"""Standard interfaces for filtering company data.

The all-important `company.Company` Facade next door offers filtering
methods that return filings and transactions that are of interest to the
caller.  Since this filtering logic is in no way stateful, however, we
implement it here as pure functions, which are then called inside of the
class methods.

"""
def filter_filings(seq, form=None, period=None):
    """Generate a list of filings in `seq` that match the criteria."""

    if form is not None:
        seq = (f for f in seq if f.region == form.region
                             and f.name == form.name)

    if period is not None:
        seq = (f for f in seq if f.period == unicode(period))

    return seq


def filter_transactions(seq, within=None, debit_type=None, credit_type=None):
    """Generate a list of transactions in `seq` that match the criteria."""

    if within is not None:
        period = within
        seq = (t for t in seq if period.start <= t.date <= period.end)

    if debit_type is not None:
        seq = (t for t in seq if t.debit_account.type == debit_type)

    if credit_type is not None:
        seq = (t for t in seq if t.credit_account.type == credit_type)

    return seq
