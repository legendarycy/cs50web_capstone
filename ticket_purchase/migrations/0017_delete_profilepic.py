# Generated by Django 4.2 on 2023-06-09 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_purchase", "0016_movies_cast_movies_director_movies_genre_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="ProfilePic",),
    ]
