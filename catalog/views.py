from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Movie, Category


class MovieList(ListView):
    queryset = (
        Movie.objects.select_related('category')
    )
    template_name = 'catalog/movies_list.html'
    context_object_name = 'movies'
    extra_context = {'page': 'index'}


class CategoryMovieList(MovieList):
    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['category_url'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(url=self.kwargs['category_url'])
        return context


class MovieDetail(DetailView):
    template_name = 'catalog/movie_detail.html'

    def get_object(self, queryset=None):
        return Movie.objects.get(url=self.kwargs['movie_url'])