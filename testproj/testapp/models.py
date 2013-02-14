from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200, default=None)


class Movie(models.Model):
    title = models.CharField(max_length=200, default=None)
    actors = models.ManyToManyField(Actor, through='Role', related_name='movies')


class Role(models.Model):
    actor = models.ForeignKey(Actor)
    movie = models.ForeignKey(Movie)


class MegaModel(models.Model):
    big_integer = models.BigIntegerField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=200)
    comma_separated_integers = models.CommaSeparatedIntegerField(max_length=200)
    date = models.DateField()
    date_time = models.DateTimeField()
    decimal = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.EmailField()
    file = models.FileField(upload_to='/')
    file_path = models.FilePathField()
    floatx = models.FloatField()
    generic_ip_address = models.GenericIPAddressField()
    image = models.ImageField(upload_to='/')
    integer = models.IntegerField()
    ip_address = models.IPAddressField()
    null_boolean = models.NullBooleanField()
    positive_integer = models.PositiveIntegerField()
    positive_small_integer = models.PositiveSmallIntegerField()
    slug = models.SlugField()
    small_integer = models.SmallIntegerField()
    text = models.TextField()
    time = models.TimeField()
    url = models.URLField()