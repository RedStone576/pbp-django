import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .utils import get_model_form

# nice read: https://docs.djangoproject.com/en/5.0/_modules/django/views/decorators/http/#require_http_methods

### ok so this one will handle ALL the cruds request, i hope its general enough but we'll see
### its really really messy rn but i'll clean it later, in like a year or two LOL
### item_type: experience | education | projects
### update with `?id=somethingidk`

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def api_view(request, item_type):
    Model, FormClass = get_model_form(item_type)

    if request.method == "GET":
        title_query = request.GET.get("title", "").strip()
        items = Model.objects.all()

        if title_query:
            if item_type == "education":
                items = items.filter(program__icontains=title_query)
            else:
                items = items.filter(title__icontains=title_query)

        if item_type == "projects":
            items = items.prefetch_related('starred_by')

        items_json = serializers.serialize("json", items, use_natural_foreign_keys=True)
        data = json.loads(items_json)

        if item_type == "projects":
            for i, item in enumerate(items):
                starred_users = item.starred_by.all()

                data[i]["fields"]["star_count"] = starred_users.count()
                data[i]["fields"]["is_starred"] = request.user in starred_users if request.user.is_authenticated else False
                data[i]["fields"]["starred_by_names"] = ", ".join([balls.username for balls in starred_users])

        elif item_type == "experience":
            for i, item in enumerate(items):
                data[i]["fields"]["category_display"] = item.get_category_display()

        return JsonResponse(data, safe=False)

    if request.method == "POST":
        if not (request.user.is_authenticated and request.user.is_superuser):
            return JsonResponse({"error": "GO AWAY !!!"}, status=403)

        form = FormClass(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"id": str(obj.id), "success": True}, status=201)

        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    ##
    _pk = request.GET.get("id")
    if not _pk:
        return JsonResponse({"error": "id required"}, status=400)

    obj = get_object_or_404(Model, id=_pk)
    ##

    if request.method == "PUT":
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name="Editor").exists())):
            return JsonResponse({"error": "GO AWAY !!!"}, status=403)

        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    # i love django man
    if request.method == "DELETE":
        if not (request.user.is_authenticated and request.user.is_superuser):
            return JsonResponse({"error": "GO AWAY !!!"}, status=403)

        obj.delete()
        return JsonResponse({"success": True})
