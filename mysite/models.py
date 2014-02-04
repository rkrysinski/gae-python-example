from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django.forms.fields import MultipleChoiceField, ChoiceField

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

class MenuItem(db.Model):
    name          = db.StringProperty(required=True)
    level         = db.StringProperty(choices=MENU_LEVEL_CHOICES)
    visible       = db.BooleanProperty(default=False)
    sub_menu      = db.ListProperty(db.Key, default=[])
    article       = db.ReferenceProperty(Article)

    def get_sub_menu(self):
        return MenuItem.get(self.sub_menu)
    
class ListPropertyChoice(MultipleChoiceField):
    def clean(self, value):
        """ extending the clean method to work with GAE keys """
        new_value = super(ListPropertyChoice, self).clean(value)
        key_list = []
        for k in new_value:
            key_list.append(db.Model.get(k).key())
        return key_list
    
    def validate(self, value):
        if value:
            super(ListPropertyChoice, self).validate(value)
    
class MenuItemForm(djangoforms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        level = int(self.initial.get('level') or self.data.get('level')) + 1
        self.fields['sub_menu'] = ListPropertyChoice(choices = [(m.key(), m.name) for m in MenuItem.all().filter("level = ", str(level)).run()])
        self.fields['level'].widget.attrs['disabled'] = True
                   
    class Meta:
        model = MenuItem

class SelectChoiceForm(djangoforms.ModelForm):
    level = ChoiceField(choices = ([(x, x) for x in  MENU_LEVEL_CHOICES]), required = True)
    