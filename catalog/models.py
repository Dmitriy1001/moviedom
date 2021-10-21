from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(unique=True, max_length=255, verbose_name='Ссылка')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(unique=True, max_length=255, verbose_name='Ссылка')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'жанр'
        verbose_name = 'жанры'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(unique=True, max_length=255, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'страну'
        verbose_name = 'страны'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО')
    url = models.SlugField(unique=True, max_length=255, verbose_name='Ссылка', null=True)
    photo = models.ImageField(upload_to='actors', blank=True, null=True, verbose_name='Фото')
    about = models.TextField(blank=True, verbose_name='Биография')

    class Meta:
        verbose_name = 'актера'
        verbose_name_plural = 'актеры'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО')
    url = models.SlugField(unique=True, max_length=255, verbose_name='Ссылка', null=True)
    photo = models.ImageField(upload_to='directors', blank=True, null=True, verbose_name='фото')
    about = models.TextField(blank=True, verbose_name='биография')

    class Meta:
        verbose_name = 'режиссера'
        verbose_name_plural = 'режиссеры'

    def __str__(self):
        return self.name


class Movie(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='movies',
        null=True,
        verbose_name='Категория',
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')
    tagline = models.CharField(max_length=255, blank=True, verbose_name='Слоган')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='movies', verbose_name='Постер')
    year = models.PositiveSmallIntegerField(default=timezone.now().year, verbose_name='Год')
    country = models.ManyToManyField(Country, related_name='movies', verbose_name='Страна')
    director = models.ManyToManyField(Director, related_name='movies', verbose_name='Режиссер')
    actors = models.ManyToManyField(Actor, related_name='movies', verbose_name='Актеры')
    genre = models.ManyToManyField(Genre, related_name='movies', verbose_name='Жанры')
    world_premiere = models.DateField(null=True, verbose_name='Премьера в мире')
    budget = models.PositiveIntegerField(default=0, help_text='сумма в $', verbose_name='Бюджет')
    fees = models.PositiveIntegerField(default=0, help_text='сумма в $', verbose_name='Сборы')
    moderation = models.BooleanField(default=False, verbose_name='Модерация')

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'movie_url': self.url})

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)

    def __str__(self):
        return self.title


class MovieShot(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE,
        related_name='shots',
        verbose_name='Фильм'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='movie_shots', verbose_name='Изображение')

    class Meta:
        verbose_name = 'кадр из фильма'
        verbose_name_plural = 'кадры из фильма'

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0, unique=True, verbose_name='Значение')

    class Meta:
        verbose_name = 'звезду рейтинга'
        verbose_name_plural = 'здезды рейтинга'
        ordering = ('-value',)

    def __str__(self):
        return str(self.value)


class Rating(models.Model):
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'

    def __str__(self):
        return f'{self.movie} - {self.star}'


class Review(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(
        Movie,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Фильм'
    )
    email = models.EmailField(blank=True, verbose_name='Почта')
    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Текст')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
        verbose_name='Ответ на комментарий',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-posted',)

    def __str__(self):
        return (
                f'{self.name} про "{self.movie}" - '
                f'{self.posted.strftime("%d %b %Yг. %H:%M")}'
        )





