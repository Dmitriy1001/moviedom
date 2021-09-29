from django.shortcuts import render
from django.views.generic import ListView

from .models import Movie


class MovieList(ListView):
    queryset = (
        Movie.objects.select_related('category')
        .prefetch_related('country', 'director', 'actors', 'genre')
    )
    template_name = 'catalog/movies_list.html'
    context_object_name = 'movies'

