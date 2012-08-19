"""Classes that represent how a tax return might be filled out and filed.

These classes are simple data containers, produced by tax forms.  When
the form registry is asked for a particular form, and then the resulting
`Form` is asked to tally up a return for a particular period, the result
is a `Filing` object, probably instantiated directly from this module
without customization.  The database code in the accompanying `model`
module has a scheme for persisting filings to the database, so that we
can remember exactly how the user filled out each tax form in the past.

"""
class Filing(object):
    """An instance of a form, computed for a particular period of time.

    The key distinction here is that 941 is a form, whereas the
    particular copy of 941 that you submitted for 2012-Q1 is a specific
    `Filing` of that form.

    """
    date = None   # for "ideal" filings; "real" filings have a value
    form = None
    period = None
    pages = ()    # in practice, replace this with a mutable list

    def new_page(self, number):
        """Constructor called by tally functions to insert a new page.

        Our list of pages is maintained in the order they were created,
        since some tax forms will require pages to be out-of-order or
        will need a single page to be duplicated several times; a list,
        unlike a dictionary indexed by page number, permits all such
        possibilities.

        """
        p = Page(number)
        self.pages.append(p)
        return p


class Page(object):
    """`Filing` sub-object that holds fields to be written to a page.

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
