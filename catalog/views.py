import re

from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ReviewForm, RatingForm
from .models import Movie, Category, Genre, Country, Director, Actor, Rating


class MovieList(ListView):
    model = Movie
    paginate_by = 9
    template_name = 'catalog/movies_list.html'
    extra_context = {'page': 'index', 'params': '?page', 'index_page': True}

    def add_average_rating(self, queryset):
        for movie in queryset:
            rating_list = [rating.star.value for rating in movie.rating.all()]
            try:
                movie.rating_av = round(sum(rating_list) / len(rating_list))
            except ZeroDivisionError:
                movie.rating_av = 0
        return queryset

    def get_queryset(self):
        movies = Movie.objects.prefetch_related('rating')
        return self.add_average_rating(movies)


class FilterMovieList(MovieList):
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
        movies = model_instance.movies.all()
        return self.add_average_rating(movies)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page'] = 'category'
        context['title'] = self.kwargs['title']
        context['params'] = '?page'
        return context


class MultipleFilterMovieList(MovieList):
    def get_queryset(self):
        genre = self.request.GET.getlist('genre')
        year = self.request.GET.getlist('year')
        if genre and not year:
            queryset = Movie.objects.filter(genre__in=genre)
        elif not genre and year:
            queryset = Movie.objects.filter(year__in=year)
        elif genre and year:
            queryset = Movie.objects.filter(year__in=year, genre__in=genre)
        movies = queryset.distinct()
        return self.add_average_rating(movies)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        params = re.search(r'/multiple_filter/(.+)', self.request.get_full_path())
        context['params'] = params.group(1) + '&page'
        return context


class SearchMovieList(MovieList):
    def get_queryset(self):
        try:
            query = self.request.GET['search'].strip()
        except KeyError:
            query = ''
        movies = Movie.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
        return self.add_average_rating(movies)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        context['page'] = 'search'
        context['search_query'] = query if query else 'Ничего не найдено'
        context['title'] = f'{query}'
        context['params'] = f'?search={query}&page'
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category'
        context['title'] = self.get_object().category.name
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        print(request.META)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(ip)
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


