from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ReviewForm, RatingForm
from .models import Movie, Category, Genre, Country, Director, Actor, Rating


class MovieList(ListView):
    model = Movie
    queryset = (
        Movie.objects.select_related('category').filter(moderation=True)
    )
    paginate_by = 3
    template_name = 'catalog/movies_list.html'
    extra_context = {'page': 'index'}


class FilterMovieList(MovieList):
    paginate_by = 1
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page'] = 'category'
        context['title'] = self.kwargs['title']
        return context


class MultipleFilterMovieList(ListView):
    def get_queryset(self):
        genre = self.request.GET.getlist('genre')
        year = self.request.GET.getlist('year')
        if genre and not year:
            queryset = Movie.objects.filter(genre__in=genre)
        elif not genre and year:
            queryset = Movie.objects.filter(year__in=year)
        elif genre and year:
            queryset = Movie.objects.filter(year__in=year, genre__in=genre)
        return queryset.distinct().values('title', 'tagline', 'url', 'poster')

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies': queryset}, safe=False)


class SearchMovieList(MovieList):
    paginate_by = 3

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
        context['page'] = 'search'
        context['search_query'] = query if query else 'Ничего не найдено'
        context['title'] = f'Поиск "{query}"'
        print(dir(self.request))
        print(query)
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
        context['movie_detail'] = True
        context['star_form'] = RatingForm()
        return context


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
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


