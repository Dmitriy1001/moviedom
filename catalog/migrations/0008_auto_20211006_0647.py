# Generated by Django 3.2.7 on 2021-10-06 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_movie_trailer_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='url',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies', to='catalog.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на трейлер'),
        ),
    ]