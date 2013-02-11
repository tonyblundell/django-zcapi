from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200)
    movies = models.ManyToManyField('Movie', through='Role', related_name='actors')


class Movie(models.Model):
    title = models.CharField(max_length=200)


class Role(models.Model):
    actor = models.ForeignKey(Actor)
    movie = models.ForeignKey(Movie)
