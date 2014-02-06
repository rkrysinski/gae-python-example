from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from mysite.models import MenuItem, MENU_LEVEL_CHOICES
from django.forms.fields import MultipleChoiceField, ChoiceField, CharField
    
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
        self.fields['sub_menu'].widget.attrs['class'] = "sub_menu"
        self.fields['level'].widget.attrs['disabled'] = True
                   
    class Meta:
        model = MenuItem

class SelectChoiceForm(djangoforms.ModelForm):
    level = ChoiceField(choices = ([(x, x) for x in  MENU_LEVEL_CHOICES]), required = True)
    
class AddImmageForm(djangoforms.ModelForm):
    urlfetch = CharField(required = True)    
    