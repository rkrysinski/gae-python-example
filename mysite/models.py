from google.appengine.ext import db
from google.appengine.api import urlfetch
from django.template.defaultfilters import slugify
urlfetch.set_default_fetch_deadline(45)

MENU_LEVEL_CHOICES=('1', '2', '3')

#https://developers.google.com/appengine/articles/modeling
#http://brizzled.clapper.org/blog/2008/08/07/writing-blogging-software-for-google-app-engine/
#https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses

class Greeting(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def get_key_from_name(cls, guestbook_name=None):
        return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')
    
class Article(db.Model):
    title         = db.StringProperty(required=True)
    body          = db.TextProperty()
    url_slug      = db.StringProperty()
    displayCount  = db.IntegerProperty(default=0)
    modified_when = db.DateTimeProperty(auto_now_add=True)

    def put(self, *args, **kwargs):
        self.url_slug = str(slugify(self.title))
        super(Article, self).put(*args, **kwargs)
        
    @classmethod
    def get_all(cls):
        return [x for x in Article.all()]
    
    @classmethod
    def get_by_slug(cls, slug):
        result = db.GqlQuery("SELECT * FROM Article WHERE url_slug = :1 LIMIT 1", slug).fetch(1)
        if (len(result) > 0):
            return result[0]
        else:
            return None           
    
class MenuItem(db.Model):
    name          = db.StringProperty(required=True)
    level         = db.StringProperty(choices=MENU_LEVEL_CHOICES)
    visible       = db.BooleanProperty(default=False)
    sub_menu      = db.ListProperty(db.Key, default=[])
    article       = db.ReferenceProperty(Article)

    def get_sub_menu(self):
        return MenuItem.get(self.sub_menu)
    
    @classmethod
    def get_all(cls):
        return [x for x in MenuItem.all().order("level")]   
    
    @classmethod
    def get_root_elements(cls):
        return [x for x in MenuItem.all().filter("level = ", MENU_LEVEL_CHOICES[0]).run()]
    
