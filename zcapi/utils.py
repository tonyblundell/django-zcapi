from django.core import serializers
from django.db import models
from django.http import Http404, HttpResponse, HttpResponseNotFound
import json


class JsonResponse(HttpResponse):
    """
        Subclass of HttpResponse which converts it's content
        to JSON format when initiated.
        If the content is a model, we return the result of its
        objects.all queryset.
    """

    def __init__(self, content='', *args, **kwargs):
        kwargs['mimetype'] = 'application/json'
        super(JsonResponse, self).__init__(*args, **kwargs)
        if isinstance(content, models.Model):
            content = to_dict(content)
        elif isinstance(content, models.base.ModelBase):
            content = [to_dict(o) for o in content.objects.all()]
        self.content = json.dumps(content)


def empty_response_on_404(f):
    """
        View Wrapper that catches Http404 exceptions and returns
        a response with an emtpy body.
    """
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Http404:
            return HttpResponseNotFound()
    return wrapped


def get_model_or_404(app, model):
    """
        Accepts an app and model name. Returns the model class if it
        exists, otherwise raises an Http404 exception.
    """
    model = models.get_model(app, model)
    if not model:
        raise Http404
    return model


def to_dict(obj, parent=None):
    """
        Utility function for converting a django object to a dictionary.
        Converts regular fields to unicode strings.
        Recursively calls relational fields.
        Includes every instance in the field.all() queryset if the field has one.
    """
    d = {}
    for field_name in obj._meta.get_all_field_names():
        try:
            field = getattr(obj, field_name)
        except AttributeError:
            pass
        else:
            if isinstance(field, models.Manager):
                if field.model != parent.__class__:
                    d[field_name] = [to_dict(o, obj) for o in field.all()]
            elif isinstance(field, models.Model):
                d[field_name] = to_dict(field, obj)
            else:
                d[field_name] = unicode(field)
    return d