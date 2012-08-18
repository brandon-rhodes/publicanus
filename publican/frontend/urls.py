from django.conf.urls import patterns, url

urlpatterns = patterns(
    'publican.frontend.views',
    url(r'^$', 'index'),
    url(r'^(\w+)/(\w+)/([-\w]+)/$', 'filing', name='filing'),
    )
