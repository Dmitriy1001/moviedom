# Generated by Django 3.2.7 on 2021-10-31 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_alter_rating_ip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('-id',), 'verbose_name': 'фильм', 'verbose_name_plural': 'фильмы'},
        ),
    ]
