from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from zcapi.utils import empty_response_on_404, get_model_or_404, JsonResponse


@empty_response_on_404
def api(request, app, model, pk=None):
    """
        The main API view.
        A model (including app) must be specified.
        An the optional instance is not specified (by PK), we operate on
        the models entire collection.
        Accepts GET, POST (for create and update) and DELETE requests.
        Returns in JSON format.
    """

    # Return a 404 if the model or instance don't exist
    model = get_model_or_404(app, model)
    obj = get_object_or_404(model, pk=pk) if pk else None

    # GET request - if an instance is specified return it,
    # otherwise return all model instances.
    if request.method == 'GET':
        return JsonResponse(obj or model)

    # POST request - if an instance is specified update it,
    # otherwise create a new one. Return the instance.
    elif request.method == 'POST':
        obj = obj or model()
        fields = [f.name for f in obj._meta.fields]
        for field in set(fields).intersection(set(request.POST)):
            setattr(obj, field, request.POST[field])
        obj.save()
        return JsonResponse(obj)

    # DELETE request - if an instance is specified delete it,
    # otherwise delete all the model instances. Return an emtpy response.
    elif request.method == 'DELETE':
        if obj:
            obj.delete()
        else:
            model.objects.all().delete()
        return JsonResponse()

    # Unrecognized request type, return a 404.
    else:
        raise Http404