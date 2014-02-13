import logging
from command import Command

class Parents(Command):
        
    def execute(self):
        logging.info("dict: %s" % self.__dict__)
        
        response = {}
        
        response['tree'] = {}
        
        import pprint
        logging.info("Parents resposne: \n%s" % pprint.pformat(response))
        
        return response

                
            
            
