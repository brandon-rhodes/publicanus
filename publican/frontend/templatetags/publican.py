"""Template tags for Publican."""

import sys
from decimal import Decimal

from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def href(obj):
    """Lets the URL to an object be constructed with {{ obj|link }}.

    This encapsulates our URL-building logic, in contrast to the shoddy
    Django practice of littering templates with {% url %} calls that
    have to all be hand-edited when a view name changes or needs to take
    different parameters: {% url 'path.to.some_view' v1 v2 %}

    """
    common = sys.modules['publican.forms.common']  # avoid weird ImportError

    if isinstance(obj, common.Filing):
        region = obj.form.__name__.split('.')[-2]
        name = obj.form.name
        return reverse('filing', args=(region, name, unicode(obj.period)))
    else:
        raise ValueError('cannot build a URL for {}.{} objects'.format(
                type(obj).__module__, type(obj).__name__))


@register.filter
def is_decimal(obj):
    """Decide whether the object is a Decimal value."""

    return isinstance(obj, Decimal)
