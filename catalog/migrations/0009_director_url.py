# Generated by Django 3.2.7 on 2021-10-06 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20211006_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='url',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='Ссылка'),
        ),
    ]
