from django import template
from catalog.models import Category, Genre, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()


@register.simple_tag()
def get_years():
    return sorted(set((movie.year for movie in Movie.objects.all())), reverse=True)


@register.simple_tag()
def get_last_movies():
    return Movie.objects.all()[:5]


