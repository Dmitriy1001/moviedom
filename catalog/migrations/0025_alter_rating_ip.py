# Generated by Django 3.2.7 on 2021-10-31 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_alter_rating_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='ip',
            field=models.CharField(max_length=15, verbose_name='IP адрес'),
        ),
    ]
