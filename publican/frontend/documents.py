"""Views that know how to generate non-HTML documents.

To prevent confusion, we keep special views like this separate from the
template-driven bread-and-butter views over in views.py.

"""
from django.http import Http404, HttpResponse
from reportlab.pdfgen import canvas

from publican.engine.kit import get_period
from publican.forms import registry


def pdf(request, region, name, period_name):
    """Generate and return a PDF for the given tax form."""

    company = request.company
    form = registry.get_form(region, name)
    period = get_period(period_name, None)
    if form is None or period is None:
        raise Http404

    c = canvas.Canvas("hello.pdf")
    c.drawString(100,700,"Hello World")
    c.showPage()

    return HttpResponse(c.getpdfdata(), content_type='application/pdf')
