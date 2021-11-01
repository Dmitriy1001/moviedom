from modeltranslation.translator import register, TranslationOptions

from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'about')


@register(Director)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('name', 'about')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'poster')
