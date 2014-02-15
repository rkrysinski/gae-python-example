from django.conf.urls.defaults import patterns
from images.views import image, tmb

urlpatterns = patterns('',
    (r'/tmb/(?P<key>[\w-]+)', tmb),    
    (r'/(?P<title>.+)', image),
)
