from django.conf.urls import patterns, url

urlpatterns = patterns(
    'publican.frontend',
    url(r'^$', 'views.index'),
    url(r'^accounts/login/$', 'demo.welcome_page'),
    url(r'^accounts/logout/$', 'demo.goodbye_page'),
    url(r'^accounts/create_demo/$', 'demo.create_demo'),
    url(r'^ledger/$', 'views.ledger'),
    url(r'^(\w+)/(\w+)/([-\w]+)/$', 'views.filing', name='filing'),
    url(r'^(\w+)-(\w+)-([-\w]+)\.pdf$', 'documents.pdf', name='pdf'),
    )
