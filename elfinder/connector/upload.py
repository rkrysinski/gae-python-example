import logging
from mysite.models import Movie
from command import Command

class Upload(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        
        response = {}
        
        if self.files:
            
            added = []
            for upload in self.files.getlist("upload[]"):
                logging.info("upload %s" % upload)
                m = Movie()
                m.upload_content(upload)
                m.put()
                Movie.get(m.key())
                added.append(m)    
            
            response["added"] = self.get_files_and_dirs(added)
            
        else:
            response = Command.get_error("Invalid backend configuration: faild to upload picture")
        
        import pprint
        logging.info("Uploae resposne: \n%s" % pprint.pformat(response))
        
        return response

                
            
            
