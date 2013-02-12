from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    actors = models.ManyToManyField(Actor, through='Role', related_name='movies')


class Role(models.Model):
    actor = models.ForeignKey(Actor)
    movie = models.ForeignKey(Movie)