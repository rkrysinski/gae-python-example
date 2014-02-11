import logging
import time
from mysite.models import Movie
import sys

ROOT_FOLDER_HASH = "DB_"
ROOT_FOLDER_NAME = "GAE DB"
VOLUME_ID = "_l1"

class Open:
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        response = {}
        
        if self.is_param_true("init"):
            
            response['api'] = self.get_api()
            response['options'] = self.get_options()
            response['uplMaxSize'] = "16M"
            
        if self.is_param_true("tree"):
            
            response['files'] = self.get_files_and_dirs()
            
        if self.is_param_true("target"):
            
            response['files'] = self.get_target(self.target)
            
        response['cwd'] = self.get_cwd()
        
        import pprint
        logging.info("resposne: %s" % pprint.pprint(response))
        return response
            
    def get_api(self):
        return "2.0"
        
    def get_options(self):
        return {
            "url"          : "/images/",
            "tmbUrl"       : "/tmb/",
            "disabled"     : [],
            "separator"    : "/",
            "archivers": {
                "create" : [],
                "extract": [],
            }
        }
        
    def get_files_and_dirs(self):
        files = []
        files.append(self.get_cwd())
        for picture in Movie.get_all():
            files.append({
                "mime": "image/jpeg",
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
        
    def get_target(self, target):
        None
            
    def get_cwd(self):
        return {
            "name"    : ROOT_FOLDER_NAME,
            "mime"    : "directory",
            "dirs"    : 0,
            "ts"      : int(time.time()),
            "hash"    : ROOT_FOLDER_HASH,
            "read"    : 1,
            "write"   : 1,
            "size"    : 0,
        }
    
    def is_param_true(self, member_name):
        member = self.__dict__.get(member_name)
        
        logging.info("member: %s" % member)
        if member:
            if type(member) == list and len(member) > 0 and member[0] == "1":
                return True
            else:
                return member
        return False
                
            
            
