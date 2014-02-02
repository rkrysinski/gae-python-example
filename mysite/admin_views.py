from django.shortcuts import render_to_response
from django.template import RequestContext
from models import MenuItem, MenuItemForm, SelectChoiceForm
from django.shortcuts import redirect
import logging

def main(request):
    template_values = MenuItem.all()
    return render_to_response('admin_page.html', template_values, context_instance=RequestContext(request))

def menu_add(request):
    isInitial = False
    level = request.POST.get('level_selection')
    if not request.POST.get('level') and not level:
        formset = SelectChoiceForm()
        isInitial = True
    elif request.POST.get('initial') == "True":
        level = request.POST.get('level')
        formset = MenuItemForm()
    elif request.method == 'POST':
        formset = MenuItemForm(request.POST)
        if formset.is_valid():
            instance = formset.save()
            MenuItem.get(instance.key()) # for refreshing purposes http://stackoverflow.com/questions/15773892/should-i-expect-stale-results-after-redirect-on-local-environment
            return redirect(menu_list)
    return render_to_response("add_menu.html", {        
                                    "formset": formset,
                                    "initial": isInitial,
                                    "level"  : level,
                              }, context_instance=RequestContext(request))    

def menu_list(request):
    return render_to_response("list_menu.html", {        
                                    "menus": MenuItem.all(),
                              }, context_instance=RequestContext(request))      
    
def menu_edit(request, key=None):
    if not key:
        return redirect(menu_list)
    m = MenuItem.get(key)
    if request.method == 'POST':
        formset = MenuItemForm(request.POST, instance=m)
        if formset.is_valid():
            formset.save()
            return redirect(menu_list)
    else:
        formset = MenuItemForm(instance=m)
    return render_to_response("add_menu.html", {        
                                    "formset": formset,
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
    