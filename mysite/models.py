from google.appengine.ext import db

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

class MenuItem(db.Model):
    name     = db.StringProperty(required=True)
    url_slug = db.StringProperty()
    visible  = db.BooleanProperty(required=True, default=False)
    sub_menu = db.ListProperty(db.Key)
    
