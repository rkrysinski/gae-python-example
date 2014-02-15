import logging
from images.models import Picture
from command import Command

class Upload(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        
        response = {}
        
        if self.files:
            
            added = []
            for upload in self.files.getlist("upload[]"):
                logging.info("upload %s" % upload)
                m = Picture()
                m.upload_content(upload)
                m.put()
                Picture.get(m.key())
                added.append(m)    
            
            response["added"] = self.get_files_and_dirs(added)
            
        else:
            response = Command.get_error("Faild to upload picture, maximum upload data must not exceed 2.5MB") # settings.py:FILE_UPLOAD_MAX_MEMORY_SIZE
        
        import pprint
        logging.info("Uploae resposne: \n%s" % pprint.pformat(response))
        
        return response

                
            
            
