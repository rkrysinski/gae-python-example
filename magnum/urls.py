from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^', include('guestbook.urls')),
)