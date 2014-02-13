import logging
from mimetypes import MimeTypes
import urllib 
import time
import sys
mime = MimeTypes()

ROOT_FOLDER_HASH = "DB_"
ROOT_FOLDER_NAME = "GAE DB"
VOLUME_ID = "_l1"

class Command:
    
    files = None
    
    def set_uploaded_files(self, files):
        self.files = files

    def get_files_and_dirs(self, pictures):
        files = []
        for picture in pictures:
            files.append({
                "mime": Command.guess_image_mime_type(picture.title),
                "ts": int(time.time()),
                "read": 1,
                "write": 1,
                "size": sys.getsizeof(picture.picture),
                "hash": "%s" % picture.key(),
                "volumeid": VOLUME_ID,
                "name": picture.title,
                "phash" : ROOT_FOLDER_HASH,
                "tmb" : "%s" % picture.key(),
            })
        return files
            
    def is_param_true(self, member_name):
        member = self.get(member_name)
        
        logging.info("%s->%s" % (member_name, member))
        if member or not "None":
            if member == "0":
                return False
            else:
                return True
        return False
        
    def get(self, member_name):
        member = self.__dict__.get(member_name)
        if type(member) == list:
            return member[0]
        return member

    def getlist(self, member_name):
        return self.__dict__.getlist(member_name)
        
    @staticmethod
    def guess_image_mime_type(filename):
        url = urllib.pathname2url(filename)
        mime_type = mime.guess_type(url)        
        return mime_type[0]
                
    @staticmethod
    def get_error(message):
        return {"error" : message }
            
            
