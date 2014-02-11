from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from elfinder.connector.dispatcher import Dispatcher

def elfinder(request):
    return render_to_response('elfinder_main.html', {}, context_instance=RequestContext(request))

def connector(request):
    cmd = Dispatcher.dispatch(request)
    response = HttpResponse(mimetype='application/json')
    response.content = json.dumps(cmd.execute())
    return response    
