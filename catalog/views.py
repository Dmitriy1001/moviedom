from django.db.models import Q
from django.views.generic import ListView, DetailView

from .mixins import ModelMovieListMixin
from .models import Movie, Category, Genre, Country, Director, Actor


class MovieList(ListView):
    queryset = (
        Movie.objects.select_related('category')
    )
    template_name = 'catalog/movies_list.html'
    context_object_name = 'movies'
    extra_context = {'page': 'index'}


class CategoryMovieListMixin(ModelMovieListMixin, MovieList):
    model = Category


class GenreMovieList(ModelMovieListMixin, MovieList):
    model = Genre


class CountryMovieList(ModelMovieListMixin, MovieList):
    model = Country


class DirectorMovieList(ModelMovieListMixin, MovieList):
    model = Director


class ActorMovieList(ModelMovieListMixin, MovieList):
    model = Actor


class SearchMovieList(MovieList):
    def get_queryset(self):
        try:
            query = self.request.GET['search'].strip()
        except KeyError:
            query = ''
        if query:
            return Movie.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        context['search_query'] = query if query else 'Ничего не найдено'
        return context


class MovieDetail(DetailView):
    template_name = 'catalog/movie_detail.html'

    def get_object(self, queryset=None):
        return Movie.objects.get(url=self.kwargs['movie_url'])