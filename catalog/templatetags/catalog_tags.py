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
    return Movie.objects.values('year').distinct().order_by('-year')


@register.simple_tag()
def get_last_movies():
    return Movie.objects.order_by('-id')[:5]


