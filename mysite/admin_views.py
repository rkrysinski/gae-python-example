from django.shortcuts import render_to_response
from django.template import RequestContext
from models import MenuItem, Movie, Article
from forms import MenuItemForm, SelectChoiceForm, AddImmageForm
from django.shortcuts import redirect

def main(request):
    return render_to_response('admin_page.html', {}, context_instance=RequestContext(request))

#######################################################
# MenuItems related handlers.
#######################################################
def menu_add(request, url_level=None):
    isInitial = False
    level = request.POST.get('level') or url_level or ""
    if not level:
        formset = SelectChoiceForm()
        isInitial = True
    elif request.POST.get('initial') == "True" or url_level:
        formset = MenuItemForm(initial={'level': level})
    elif request.method == 'POST':
        formset = MenuItemForm(request.POST)
        if formset.is_valid():
            instance = formset.save()
            MenuItem.get(instance.key()) # for refreshing purposes http://stackoverflow.com/questions/15773892/should-i-expect-stale-results-after-redirect-on-local-environment
            return redirect(menu_list)
    return render_to_response("menu_add.html", {        
                                    "formset": formset,
                                    "initial": isInitial,
                                    "level"  : level
                              }, context_instance=RequestContext(request))    

def menu_list(request):
    return render_to_response("menu_list.html", {        
                                    "all_items": MenuItem.get_all(),
                                    "menu" : MenuItem.get_all(filter_level=0),
                              }, context_instance=RequestContext(request))      
    
def menu_edit(request, key=None):
    if not key:
        return redirect(menu_list)
    m = MenuItem.get(key)
    if request.method == 'POST':
        formset = MenuItemForm(request.POST, instance=m)
        if formset.is_valid():
            m = formset.save()
            MenuItem.get(m.key())  # for refreshing purposes http://stackoverflow.com/questions/15773892/should-i-expect-stale-results-after-redirect-on-local-environment
            return redirect(menu_list)
    else:
        formset = MenuItemForm(instance=m)
    return render_to_response("menu_add.html", {        
                                    "formset": formset,
                                    "level"  : m.level
                              }, context_instance=RequestContext(request))     
    
def menu_delete(request, key=None):
    if not key:
        return redirect(menu_list)
    if request.POST.get('confirmation') == 'yes':
        m = MenuItem.get(key)
        if m: 
            m.delete()
            MenuItem.get(key) # for refreshing purposes http://stackoverflow.com/questions/15773892/should-i-expect-stale-results-after-redirect-on-local-environment
    if request.POST.get('confirmation'):
        return redirect(menu_list)
    return render_to_response("confirmation.html", {}, context_instance=RequestContext(request))     

#######################################################
# Image related handlers.
#######################################################

def image_add(request):
    formset = None
    urlfetch = request.POST.get('urlfetch')
    if urlfetch:
        movie = Movie()
        movie.set_content(urlfetch)
        movie.put()
        return redirect(image_list)
    else:
        formset = AddImmageForm()
        
    return render_to_response("image_add.html", {
                                    "formset" : formset
                              }, context_instance=RequestContext(request))   
    
def image_list(request):
    return render_to_response("image_list.html", {
                                    "images" : Movie.get_all(),
                              }, context_instance=RequestContext(request))    

#######################################################
# Article related handlers.
#######################################################

def article_add(request):
    return render_to_response("articles_add.html", {
                              }, context_instance=RequestContext(request))  
    
def article_list(request):
    return render_to_response("articles_list.html", {
                                    "articles" : Article.get_all(),
                              }, context_instance=RequestContext(request))  
