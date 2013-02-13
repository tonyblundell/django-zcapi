from django.core import serializers
from django.db import models
from django.http import Http404, HttpResponse, HttpResponseNotFound
import json


class JsonResponse(HttpResponse):
    def __init__(self, content='', *args, **kwargs):
        kwargs['mimetype'] = 'application/json'
        super(JsonResponse, self).__init__(*args, **kwargs)
        if isinstance(content, models.Model):
            content = to_dict(content)
        elif isinstance(content, models.base.ModelBase):
            content = [to_dict(o) for o in content.objects.all()]
        self.content = json.dumps(content)


def empty_response_on_404(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Http404:
            return HttpResponseNotFound()
    return wrapped


def get_model_or_404(app, model):
    model = models.get_model(app, model)
    if not model:
        raise Http404
    return model


def to_dict(obj, parent=None):
    d = {}
    for field_name in obj._meta.get_all_field_names():
        field = getattr(obj, field_name, None)
        if field:
            if isinstance(field, models.Manager):
                if field.model != parent.__class__:
                    d[field_name] = [to_dict(o, obj) for o in field.all()]
            elif isinstance(field, models.Model):
                d[field_name] = to_dict(field, obj)
            else:
                d[field_name] = unicode(field)
    return d