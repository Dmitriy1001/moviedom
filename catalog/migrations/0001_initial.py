# Generated by Django 3.2.7 on 2021-09-28 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('photo', models.ImageField(upload_to='actors', verbose_name='фото')),
                ('about', models.TextField(blank=True, verbose_name='биография')),
            ],
            options={
                'verbose_name': 'актера',
                'verbose_name_plural': 'актеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'страны',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('photo', models.ImageField(upload_to='directors', verbose_name='фото')),
                ('about', models.TextField(blank=True, verbose_name='биография')),
            ],
            options={
                'verbose_name': 'режиссера',
                'verbose_name_plural': 'режиссеры',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'жанры',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')),
                ('tagline', models.CharField(default='', max_length=255, verbose_name='Слоган')),
                ('description', models.TextField(verbose_name='Описание')),
                ('poster', models.ImageField(upload_to='movies', verbose_name='Постер')),
                ('year', models.PositiveSmallIntegerField(default=2021, verbose_name='Год')),
                ('world_premiere', models.DateField(null=True, verbose_name='Премьера в мире')),
                ('budget', models.PositiveIntegerField(default=0, help_text='сумма в $', verbose_name='Бюджет')),
                ('fees', models.PositiveIntegerField(default=0, help_text='сумма в $', verbose_name='Сборы')),
                ('moderation', models.BooleanField(default=False, verbose_name='Модерация')),
                ('actors', models.ManyToManyField(related_name='movies', to='catalog.Actor', verbose_name='Актеры')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.category', verbose_name='Категория')),
                ('country', models.ManyToManyField(related_name='movies', to='catalog.Country', verbose_name='Страна')),
                ('directors', models.ManyToManyField(related_name='movies', to='catalog.Director', verbose_name='Режиссер')),
                ('genres', models.ManyToManyField(related_name='movies', to='catalog.Genre', verbose_name='Жанры')),
            ],
            options={
                'verbose_name': 'фильм',
                'verbose_name_plural': 'фильмы',
            },
        ),
    ]