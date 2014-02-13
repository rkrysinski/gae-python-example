import importlib, new
import logging

class Dispatcher:
    
    @staticmethod
    def dispatch(request):
        operation = request.POST.get('cmd') 
        cmd = None
        if operation:
            try:
                logging.info("files: %s " % request.FILES)
                cmd = Dispatcher.get_class(operation, request.POST)
                cmd.set_uploaded_files(request.FILES)
            except Exception as e:
                logging.info("e: %s" % e)
        return cmd
            
    @staticmethod
    def get_class(kls, attrs):
        parts = __name__.split('.')
        module = "%s.%s" % (".".join(parts[:-1]), kls)
        m = importlib.import_module(module)
        m = getattr(m, kls.title())
        m = new.instance(m, attrs)
        return m            
    