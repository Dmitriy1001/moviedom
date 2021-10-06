from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView, DetailView


from .models import Movie, Category, Genre, Country, Director, Actor


class MovieList(ListView):
    queryset = (
        Movie.objects.select_related('category')
    )
    template_name = 'catalog/movies_list.html'
    context_object_name = 'movies'
    extra_context = {'page': 'index'}


class FilterByMovieList(MovieList):
    models = {
        'category': Category,
        'genre': Genre,
        'country': Country,
        'director': Director,
        'actor': Actor
    }

    def get_queryset(self):
        try:
            model = self.models[self.kwargs['model']]
        except KeyError:
            raise Http404
        model_instance = model.objects.get(url=self.kwargs['model_url'])
        self.kwargs['title'] = model_instance.name
        return model_instance.movies.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        return context


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