# Generated by Django 3.2.7 on 2021-10-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('-date',), 'verbose_name': 'контакт', 'verbose_name_plural': 'контакты'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
