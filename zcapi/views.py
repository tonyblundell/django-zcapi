from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from zcapi.utils import get_model_or_404, JsonResponse


def api(request, app, model, pk=None):
    model = get_model_or_404(app, model)
    obj = get_object_or_404(model, pk=pk) if pk else None

    if request.method == 'GET':
        return JsonResponse(obj or model)

    elif request.method == 'POST':
        obj = obj or model()
        fields = [f.name for f in obj._meta.fields]
        for field in set(fields).intersection(set(request.POST)):
            setattr(obj, field, request.POST[field])
        obj.save()
        return JsonResponse(obj)

    elif request.method == 'DELETE':
        if obj:
            obj.delete()
        else:
            model.objects.all().delete()
        return JsonResponse()

    else:
        raise Http404