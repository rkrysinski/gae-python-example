from django.shortcuts import redirect
from django.http import HttpResponse
from models import Picture

def image(request, title):
    img = Picture.get_picture(title)
    if (img and img.picture):
        return HttpResponse(img.picture, mimetype="image/jpeg")
    else:
        return redirect('/static/noimage.jpg')
    
def tmb(request, key):
    img = Picture.get(key)
    if img.thumbnail:
        return HttpResponse(img.thumbnail, mimetype="image/jpeg")
    else:
        return redirect('/static/noimage_tmb.jpg')
    