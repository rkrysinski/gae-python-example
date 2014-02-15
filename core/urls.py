from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^elfinder', include('elfinder.urls')),
    (r'^images', include('images.urls')),
    (r'^', include('mysite.urls')),
)