from django.conf.urls.defaults import patterns
from mysite.views import main_page, sign_post
import mysite.admin_views


urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_page),
    
    (r'^admin/menu/add/(?P<url_level>\d*)', mysite.admin_views.menu_add),
    (r'^admin/menu/list/', mysite.admin_views.menu_list),
    (r'^admin/menu/edit/(?P<key>[\w-]+)', mysite.admin_views.menu_edit),
    (r'^admin/menu/delete/(?P<key>[\w-]+)', mysite.admin_views.menu_delete),
    
    (r'^admin/image/add/', mysite.admin_views.image_add),
    (r'^admin/image/list/', mysite.admin_views.image_list),
    (r'^admin/image/upload/', mysite.admin_views.image_upload),
    (r'^admin/image/delete/(?P<key>[\w-]+)', mysite.admin_views.image_delete),
    
    (r'^admin/article/add/', mysite.admin_views.article_add),
    (r'^admin/article/list/', mysite.admin_views.article_list),
    (r'^admin/article/view/(?P<slug>.+)', mysite.admin_views.article_view),
    (r'^admin/article/delete/(?P<key>[\w-]+)', mysite.admin_views.article_delete),    
    
    (r'^admin/', mysite.admin_views.main),
)
