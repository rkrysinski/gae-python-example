from django.conf.urls.defaults import patterns
from mysite.views import main_page, sign_post
import mysite.admin_views


urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_page),
    
    (r'^admin/', mysite.admin_views.main),
)
