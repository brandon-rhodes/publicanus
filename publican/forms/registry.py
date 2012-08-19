"""The registry of all installed forms.

For the moment, this registry simply returns the forms that come
pre-installed in Publican.  In the future, when people start wanting to
contribute packages full of additional forms that they have written, we
may move to an entry-points-based solution to finding forms instead.

Note that the two public methods of this class, `all_forms()` and
`get_form()`, are the only supported means of constructing `Form`
objects.  Other code should *not* be importing `Form` directly and
trying to usefully instantiate it.

The `Form` class is an example of the Bridge design pattern: it offers
an easy-to-use interface that decouples callers from the details of how
forms are actually implemented.  Thanks to its conveniences, no other
code gets exposed to the details of we implement forms using modules.

"""
from publican.engine.filings import Filing

__all__ = ('all_forms', 'get_form')

def all_forms():
    """Return all known forms, as a list."""
    return _load().values()

def get_form(region, name):
    """Return the tax form with `name` in `region`, else return `None`."""
    key = region, name
    return _load().get(key, None)

# Private implementation.

_forms = {}

def _load():
    """Secretly import a hard-wired list of forms, kept in sync by hand."""
    if not _forms:
        from .us import form_940, form_941
        for module in form_940, form_941:
            form = Form(module)
            key = form.region, form.name
            _forms[key] = form
    return _forms

class Form(object):
    """A tax form that knows when it is due, and can compute its return.

    Note that instances of this class behave like singletons: they do
    not mutate during, or across, operations.  Its methods are purely
    functional.  This allows the registry, once it has finished loading
    and setting up a `Form`, to hand that same instance to as many
    threads as it likes without consequence.

    As a mild reminder of the fact that instances are intended to be
    read-only, it defines `__slots__` to protect code that might write
    an attribute on a `Form` that it might actually have intended for
    one of its own classes.

    """
    __slots__ = ('_module', 'region', 'name', 'title', 'grids', 'filename')

    def __init__(self, module):
        parts = module.__name__.split('.')
        self._module = module
        self.region = parts[-2]
        self.name = parts[-1].split('_', 1)[1]
        self.title = module.title
        self.grids = module.grids
        self.filename = module.filename

    def periods(self, company):
        """For what periods will the `company` have to submit this form?

        Returns a list of `publican.engine.kit.Period` objects.

        """
        return self._module.periods(company)

    def tally(self, company, period):
        """Figure out how the `company` should fill in this form for `period`.

        Returns a `Filing` object with one or more pages inside,
        illustrating how the form should be filled out.

        """
        filing = Filing()
        filing.region = self.region
        filing.name = self.name
        filing.period_name = period.name
        filing.pages = []
        return self._module.tally(company, period, filing)
