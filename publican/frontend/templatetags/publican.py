"""Template tags for Publican."""

from decimal import Decimal

from django import template
from django.core.urlresolvers import reverse

from ...engine.filings import Filing  # weird; only relative import works here

register = template.Library()
_abs = abs

@register.filter
def abs(value):
    """Discard the sign of `value`."""
    return _abs(value)


@register.filter
def href(obj):
    """Lets the URL to an object be constructed with {{ obj|link }}.

    This encapsulates our URL-building logic in one single place, in
    contrast to the usual Django practice of littering every template
    with {% url %} calls that have to all be hand-edited in the future
    when a view name changes, or needs to take different parameters.

    """
    if isinstance(obj, Filing):
        return reverse('filing', args=(obj.region, obj.name, obj.period_name))
    else:
        raise ValueError('cannot build a URL for {}.{} objects'.format(
                type(obj).__module__, type(obj).__name__))


@register.filter
def is_decimal(obj):
    """Decide whether the object is a Decimal value."""

    return isinstance(obj, Decimal)


@register.filter
def mydate(d, codes):
    format = ' '.join('%' + letter for letter in codes.split())
    return d.strftime(format).lstrip('0').replace(' 0', ' ')
