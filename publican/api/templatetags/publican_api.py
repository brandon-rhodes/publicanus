"""Template tags for using the Publican API."""

from django import template
from django.core.urlresolvers import reverse

from ...engine.filings import Filing

register = template.Library()

@register.filter
def api(obj):
    """Compute the URL to an object in the REST API.

    See the notes on the nearby `publican.href()` filter to learn why a
    unified URL-generating function like this is a good idea.

    """
    if isinstance(obj, Filing):
        region = obj.form.region
        name = obj.form.name
        date = obj.date
        return reverse('api-filing', args=(region, name, unicode(obj.period),
                                           date))
    else:
        raise ValueError('cannot build a URL for {}.{} objects'.format(
                type(obj).__module__, type(obj).__name__))
