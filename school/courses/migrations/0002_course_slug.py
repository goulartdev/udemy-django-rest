# Generated by Django 3.2.7 on 2021-09-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
