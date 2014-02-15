from google.appengine.ext import db
from google.appengine.api import images

class Picture(db.Model):
    title     = db.StringProperty()
    picture   = db.BlobProperty(default=None)
    thumbnail = db.BlobProperty(default=None)

    def upload_content(self, f):
        self.title = f.name
        self.picture = db.Blob(f.read())
        self.set_thumbnail()
        
    def set_thumbnail(self):
        if self.picture:
            tmb = images.resize(self.picture, 48, 48)
            self.thumbnail = db.Blob(tmb)
       
    @classmethod
    def get_picture(cls, title):
        result = db.GqlQuery("SELECT * FROM Picture WHERE title = :1 LIMIT 1",
                        title).fetch(1)
        if (len(result) > 0):
            return result[0]
        else:
            return None    
        
    @classmethod
    def get_all(cls):
        return [x for x in Picture.all()]   
