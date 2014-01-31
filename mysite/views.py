from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from google.appengine.api import users

from mysite.models import Greeting

import urllib

def main_page(request):
    guestbook_name = request.GET.get('guestbook_name', 'default_guestbook')
    guestbook_key = Greeting.get_key_from_name(guestbook_name)
    greetings_query = Greeting.all().ancestor(guestbook_key).order('-date')
    greetings = greetings_query.fetch(10)
    if users.get_current_user():
        url = users.create_logout_url(request.get_full_path())
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.get_full_path())
        url_linktext = 'Login'
    template_values = {
        'greetings': greetings,
        'guestbook_name': guestbook_name,
        'url': url,
        'url_linktext': url_linktext,
    }
    return render_to_response('main_page.html', template_values, context_instance=RequestContext(request))

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        guestbook_key = Greeting.get_key_from_name(guestbook_name)
        greeting = Greeting(parent=guestbook_key)
    
        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()
    
        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    return HttpResponseRedirect('/')
