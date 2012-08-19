"""Facade through which the application interacts with persisted data.

This `Company` class is an example of the Facade pattern: it offers a
simple and clean interface to a more complex reality that lies behind.

Most Publican code, including that in the `forms` library and in the
`frontend` itself, interacts only with `Company` objects, without any
thought for what lies behind them.  When those packages are under test,
there is, in fact, very little behind the `Company` object except for a
couple of lists sitting in RAM, which is why tests run very fast.

But when the application is running in production, a subclass of
`Company` that lives next door in the `models` module in fact passes the
queries it receives through to Django model objects that are persisted
in our database.

Either way, it is the interface presented here that the rest of the
application is concerned with.

"""
from . import filtering

class Company(object):
    """Entity that spends money on employees, consultants, and taxes."""

    def __init__(self, ein, name, incorporation_date):
        self.ein = ein
        self.name = name
        self.incorporation_date = incorporation_date

    # These two attributes should be set to sequences of Filing and
    # Transaction objects, either through a test manually setting them,
    # or through a database load.  The `None` value is a safe default
    # because it is not iterable, and so will cause the corresponding
    # "filter" method to fail if not initialized.

    _filings = None
    _transactions = None

    def filings(self, **kw):
        """Return all `Filing` objects matching the given constraints."""
        return filtering.filter_filings(self._filings, **kw)

    def transactions(self, **kw):
        """Return all `Transaction` objects matching the given constraints."""
        return filtering.filter_transactions(self._transactions, **kw)
