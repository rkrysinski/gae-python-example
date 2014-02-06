from django.shortcuts import redirect
from django.http import HttpResponse
from models import Movie

def get_image(request, title):
    movie = Movie.get_movie(title)
    if (movie and movie.picture):
        return HttpResponse(movie.picture, mimetype="image/jpeg")
    else:
        return redirect('/static/noimage.jpg')    
