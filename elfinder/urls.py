from django.conf.urls.defaults import patterns
from elfinder.views import elfinder, connector

urlpatterns = patterns('',
    (r'/connector/', connector),
    (r'', elfinder),
)
