"""Views that know how to generate non-HTML documents.

To prevent confusion, we keep special views like this separate from the
template-driven bread-and-butter views over in views.py.

"""
import os
from StringIO import StringIO
from django.http import Http404, HttpResponse
from pyPdf import PdfFileWriter, PdfFileReader
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

    datadir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    pdfpath = os.path.join(datadir, 'f940--2011.pdf')

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
