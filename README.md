publicanus
==========

This is the code base behind <i>Publican,</i>
a prototype small business accounting application for the web.

I have just written this Publican prototype
as my entry in the [Django Dash](http://www.djangodash.com/) 2012.
You can currently see a demonstration here:

<http://publican.rhodesmill.org>

I have tried to direct my effort towards creating
a beautiful and extensible core for further development.
There were three main ideas that I wanted this prototype to illustrate.

* The idea of the timeline that lives on the main page
  is the vision that first popped into my head, several months ago,
  and that eventually led to my choosing this project.
  It is, in miniature, exactly what I need:
  a view that lets me step back and look at the big picture
  of what tax obligations are approaching
  and what I will need to do to satisfy them.

* The interface that tax form code uses to traverse business data
  was another major focus of attention.
  The last thing I want
  is to burden the authors of future Publican tax-form modules
  with a finicky and fragile interface;
  instead, I want to hide the database from them completely,
  and give them an easy way to view its data
  without getting tangled up in ORM details.
  I also wanted tax-form computation logic to be strongly decoupled
  from the rest of the application —
  you will note,
  if you review the Python code
  for [Form 940](https://github.com/brandon-rhodes/publicanus/blob/master/publican/forms/us/form_940.py)
  and [Form 941](https://github.com/brandon-rhodes/publicanus/blob/master/publican/forms/us/form_941.py)
  that I have mocked up,
  that the interface is *completely* functional,
  and persists no state at all between calls.
  Tax form modules do not even define any classes;
  they simply define functions, along with a few data structures
  to support HTML and PDF rendering!

* The most exciting stunt, I suppose, was the code in `documents.py`
  that fills out and renders PDF tax forms,
  and it really surprised me that my scheme worked on its first try
  without any complaint.
  Some day the process might fall over
  if we try giving it some obscure state tax form
  produced by a poor PDF export program,
  but for federal forms it is a staggeringly clean process.
  The trick is that it took two separate PDF libraries
  to make the process so elegant:
  ReportLab is the expert at *producing* PDF,
  but pyPdf is the king when it comes to *assembling* documents
  out of pieces.

You can run the project tests —
which currently ignore the web interface
and instead exercise the tax form computation logic —
by checking the project out and running:

    $ python -m unittest publican.forms.us.tests

Finally, a note on terminology:
a <i>publican</i> was the Roman term for a tax collector.
You can think of Publican as an old patrician,
well versed in all of the details of tax law,
looking over your situation and helping you figure out
what needs to be filed next.

Thanks for reading, and let me know if you have any questions!
