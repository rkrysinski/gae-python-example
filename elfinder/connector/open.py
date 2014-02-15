import logging
import time
from command import Command, ROOT_FOLDER_NAME, ROOT_FOLDER_HASH
from images.models import Picture

class Open(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        response = {}
        
        if self.is_param_true("init"):
            
            response['api'] = self.get_api()
            response['options'] = self.get_options()
            response['uplMaxSize'] = "16M"
            
        if self.is_param_true("tree"):
            
            response['files'] = self.get_files_and_dirs(Picture.get_all())
            response['files'].append(self.get_cwd())
            
        elif self.is_param_true("target"):
            
            response['files'] = self.get_target(self.target)
            
        response['cwd'] = self.get_cwd()
        
        import pprint
        logging.info("resposne: \n%s" % pprint.pformat(response))
        return response
            
    def get_api(self):
        return "2.0"
        
    def get_options(self):
        return {
            "url"          : "/images/",
            "tmbUrl"       : "/images/tmb/",
            "disabled"     : [],
            "separator"    : "/",
            "archivers": {
                "create" : [],
                "extract": [],
            }
        }
        
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
                
            
            
