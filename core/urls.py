from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^elfinder', include('elfinder.urls')),
    (r'^', include('mysite.urls')),
)