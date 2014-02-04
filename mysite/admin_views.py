from django.shortcuts import render_to_response
from django.template import RequestContext
from models import MenuItem, MenuItemForm, SelectChoiceForm, MENU_LEVEL_CHOICES
from django.shortcuts import redirect

def main(request):
    template_values = MenuItem.all()
    return render_to_response('admin_page.html', template_values, context_instance=RequestContext(request))

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
    return render_to_response("add_menu.html", {        
                                    "formset": formset,
                                    "initial": isInitial,
                                    "level"  : level
                              }, context_instance=RequestContext(request))    

def menu_list(request):
    return render_to_response("list_menu.html", {        
                                    "all_items": MenuItem.all().order("level"),
                                    "menu" : [x for x in MenuItem.all().filter("level = ", MENU_LEVEL_CHOICES[0]).run()]
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
    return render_to_response("add_menu.html", {        
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
    