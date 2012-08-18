
class Filing(object):
    """An instance of a form, computed for a particular period of time.

    The key distinction here is that 941 is a form, whereas the
    particular copy of 941 that you submitted for 2012-Q1 is a specific
    `Filing` of that form.
    """
    # Building a Filing.

    def __init__(self, form, period):
        self.form = form
        self.period = period
        self.pages = []

    def tally(self, company):
        """Tally the form; results are saved to attributes of this `Page`."""
        self.form.tally(company, self)

        # TODO: make this more interesting
        # self.state = 'warn' if company.today < self.due_date else 'good'

    def new_page(self, number):
        """Constructor called by tally functions to insert a new page."""
        p = Page(number)
        self.pages.append(p)
        return p


class Page(object):
    """`Filing` sub-object; create pages through `Filing.new_page()`.

    This object is deliberately almost devoid of attributes, to stay out
    of the way of our form logic, which creates a new attribute on a
    `Page` for every tax form line that it computes.

    One attribute is special: `number` stores which page of the form
    these attributes pertain to.  When rendering the form on the web,
    the `number` acts as an index into the form's `grid`; when rendering
    the form to PDF, it acts as an index into the form's `pdf`.

    """
    def __init__(self, number):
        self.number = number
