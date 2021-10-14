from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShot, Actor, Director, Country, RatingStar, Rating, Review

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_photo')

    @admin.display(description='Фото')
    def get_photo(self, actor):
        return mark_safe(f'<img src={actor.photo.url} width="70" height="80">')


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotInline(admin.TabularInline):
    model = MovieShot
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, movie_shot):
        return mark_safe(f'<img src={movie_shot.image.url} width="120" height="120">')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'genres',
        'directors',
        'year',
        'countries',
        'get_poster',
        'moderation',
    )
    list_filter = ('category', 'year')
    search_fields = ('title', 'description')
    prepopulated_fields = {'url': ('title',)}
    inlines = (MovieShotInline, ReviewInline)
    save_on_top = True
    list_editable = ('moderation',)
    form = MovieAdminForm
    actions = ('publish', 'unpublish')

    def unpublish(self, request, queryset):
        row_update = queryset.update(moderation=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f''
        self.message_user(request, message_bit)

    def publish(self, request, queryset):
        row_update = queryset.update(moderation=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'записей обновлено - {row_update}'
        self.message_user(request, message_bit)

    def get_poster(self, movie):
        return mark_safe(f'<img src={movie.poster.url} width="70" height="80">')

    genres = lambda self, movie: ', '.join(map(str, movie.genre.all()))
    directors = lambda self, movie: ', '.join(map(str, movie.director.all()))
    countries = lambda self, movie: ', '.join(map(str, movie.country.all()))

    unpublish.short_description = 'Опубликовать'
    publish.short_description = 'Снять с публикации'
    publish.allowed_permissions = ('change',)
    unpublish.allowed_permissions = ('change',)

    get_poster.short_description = 'Постер'
    genres.short_description = 'Жанр'
    directors.short_description = 'Режисер'
    countries.short_description = 'Страна'


@admin.register(MovieShot)
class MovieShotAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image')

    @admin.display(description='Кадр')
    def get_image(self, movie_shot):
        return mark_safe(f'<img src={movie_shot.image.url} width="120" height="120">')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('movie', 'posted')
    readonly_fields = ('name', 'email')


admin.site.site_title = 'MovieDom'
admin.site.site_header = 'MovieDom'



