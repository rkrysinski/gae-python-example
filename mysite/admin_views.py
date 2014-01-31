from django.shortcuts import render_to_response
from django.template import RequestContext

def main(request):
    template_values=None
    return render_to_response('admin_page.html', template_values, context_instance=RequestContext(request))
