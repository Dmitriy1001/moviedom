from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Movie, Category, Genre, Country, Director, Actor


class MovieList(ListView):
    queryset = (
        Movie.objects.select_related('category')
    )
    template_name = 'catalog/movies_list.html'
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
            model_instance = model.objects.get(url=self.kwargs['model_url'])
        except KeyError:
            raise Http404
        except model.DoesNotExist:
            raise Http404(f'{model._meta.verbose_name} не найдено')
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
    form_class = ReviewForm

    def get_object(self, queryset=None):
        return Movie.objects.get(url=self.kwargs['movie_url'])

    def post(self, request, **kwargs):
        movie = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            if request.POST.get('parent', None):
                new_review.parent_id = int(request.POST.get("parent"))
            new_review.movie = movie
            new_review.save()
            return redirect('movie_detail', movie.url)
        return render(request, self.template_name, {'movie': movie, 'form': form})