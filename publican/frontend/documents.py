"""Views that know how to generate non-HTML documents.

To prevent confusion, we keep special views like this separate from the
template-driven bread-and-butter views over in views.py.

"""
import os
from decimal import Decimal
from django.http import Http404, HttpResponse
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from StringIO import StringIO

from publican.engine.kit import get_period
from publican.forms import registry


def pdf(request, region, name, period_name):
    """Generate and return a PDF for the given tax form."""

    company = request.company
    form = registry.get_form(region, name)
    period = get_period(period_name, None)
    if form is None or period is None:
        raise Http404

    filing = form.tally(company, period)

    c = canvas.Canvas("hello.pdf")
    for spec in form.pdf_fields:
        x, y, name = spec[:3]
        value = getattr(filing.pages[0], name, None)
        if value is None:
            value = u''
        if isinstance(value, Decimal):
            dollars, cents = unicode(value).split('.')
            c.drawString(x - 8 - c.stringWidth(dollars), y, dollars)
            c.drawString(x + 4, y, cents)
        elif len(spec) > 3:
            value = unicode(value)
            step = spec[3]
            for i, char in enumerate(value):
                c.drawString(x + i * step, y, char)
        else:
            value = unicode(value)
            c.drawString(x, y, value)

    c.showPage()

    datadir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    pdfpath = os.path.join(datadir, form.filename)

    taxform = PdfFileReader(file(pdfpath, 'rb'))
    rendering = PdfFileReader(StringIO(c.getpdfdata()))
    output = PdfFileWriter()

    watermark = rendering.getPage(0)

    page1 = taxform.getPage(0)
    page1.mergePage(watermark)
    output.addPage(page1)

    pdfdata = StringIO()
    output.write(pdfdata)

    return HttpResponse(pdfdata.getvalue(), content_type='application/pdf')
