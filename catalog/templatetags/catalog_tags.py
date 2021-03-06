from django import template

from catalog.models import Category, Genre, Movie, RatingStar

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()


@register.simple_tag()
def get_stars():
    return RatingStar.objects.all()


@register.simple_tag()
def get_years_n_last_movies():
    movies = Movie.objects.filter(moderation=True)
    return {
        'years': sorted({year['year'] for year in movies.values('year')}, reverse=True),
        'last_movies': movies[:5],
    }
