# Generated by Django 3.2.7 on 2021-10-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20211014_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='trailer_url',
        ),
        migrations.AlterField(
            model_name='rating',
            name='ip',
            field=models.CharField(max_length=15, verbose_name='IP адрес'),
        ),
    ]
