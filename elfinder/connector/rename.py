import logging
from mysite.models import Movie
from command import Command

class Rename(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        
        response = {}
        
        if self.is_param_true("target") and self.is_param_true("name"):
            m = Movie.get(self.get("target"))
            m.title = self.get("name")
            m.put()
            Movie.get(m.key())
        else:
            Command.get_error("Invalid backend configuration")
        
        import pprint
        logging.info("resposne: \n%s" % pprint.pformat(response))
        
        return response

                
            
            
