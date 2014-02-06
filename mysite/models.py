from google.appengine.ext import db
from google.appengine.api import urlfetch
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

    @classmethod
    def get_all(cls):
        return [x for x in Article.all()]

class MenuItem(db.Model):
    name          = db.StringProperty(required=True)
    level         = db.StringProperty(choices=MENU_LEVEL_CHOICES)
    visible       = db.BooleanProperty(default=False)
    sub_menu      = db.ListProperty(db.Key, default=[])
    article       = db.ReferenceProperty(Article)

    def get_sub_menu(self):
        return MenuItem.get(self.sub_menu)
    
    @classmethod
    def get_all(cls, filter_level=None):
        if filter_level:
            return [x for x in MenuItem.all().filter("level = ", MENU_LEVEL_CHOICES[filter_level]).run()]
        
        return [x for x in MenuItem.all().order("level")]   
    
    
class Movie(db.Model):
    '''
    See: https://developers.google.com/appengine/articles/python/serving_dynamic_images
    '''
    title = db.StringProperty()
    picture = db.BlobProperty(default=None)

    def set_content(self, url):
        import re
        self.title = re.search('.*/(.+\....)', url).group(1)
        self.picture = db.Blob(urlfetch.Fetch(url).content)
        
    def get_img_code(self):
        return r'<img src="/images/%s" />' % self.title
        
    @classmethod
    def get_movie(cls, title):
        result = db.GqlQuery("SELECT * FROM Movie WHERE title = :1 LIMIT 1",
                        title).fetch(1)
        if (len(result) > 0):
            return result[0]
        else:
            return None    
        
    @classmethod
    def get_all(cls):
        return [x for x in Movie.all()]   
