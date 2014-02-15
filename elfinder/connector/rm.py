import logging
from images.models import Picture
from command import Command

class Rm(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        
        response = {}
        
        if self.is_param_true("targets[]"):
            
            removed = []
            for key in self.getlist("targets[]"):
                m = Picture.get(key)
                m.delete()
                Picture.get(m.key())
                removed.append(key)
            response["removed"] = removed
            
        else:
            response = Command.get_error("Invalid backend configuration: faild to remove picture")
        
        import pprint
        logging.info("Rm resposne: \n%s" % pprint.pformat(response))
        
        return response

                
            
            
