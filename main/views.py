from django.contrib import messages
# from django.core import serializers
# from django.http import HttpResponse just so i dont forgor
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

# nice read: https://docs.djangoproject.com/en/5.0/_modules/django/views/decorators/http/#require_http_methods

from main.models import Experience, Education, Project
from main.forms import ExperienceForm, EducationForm, ProjectForm

MY_INFO = {
    "name": "Ilham Firmansyah", 
    "npm": "2506532643",
    "study_program": "Sistem Informasi",
    "study_program_kd": "06.00.12.01",
    "role": "Insinyur Perangkat Lunak",
}

###

MODELS = {
    "experience": (Experience, ExperienceForm),
    "education": (Education, EducationForm),
    "projects": (Project, ProjectForm),
}

def get_model_form(item_type):
    model, form = MODELS[item_type]
    return model, form

###

def show_main(request):
    # mkay context.name are more like title or something bruh
    context = {
        "bio": (
            "<ul>"
            "<li>Recreational programmer</li>"
            "<li>linguistic enthusiast</li>"
            "<li>supposedly computer philosopher</li>"
            "<li>and Tetris player at heart.</li>"
            "</ul>"
            "Loves raw JavaScript at its finest. TypeScript too, if you insist."
        ),
    }
    
    return render(request, "index.html", MY_INFO | context)

###

def show_list(request, item_type):
    Model, _ = get_model_form(item_type)
    context = {f"{item_type}_list": Model.objects.all()}
    return render(request, f"{item_type}.html", MY_INFO | context)

###

def form_view(request, item_type):
    Model, FormClass = get_model_form(item_type)
    
    ## dunno how to create a headless block in python, so this comments will do
    _pk = request.GET.get("id")
    
    instance = None
    
    if _pk:
        instance = get_object_or_404(Model, id=_pk)
    ##
    
    form = FormClass(request.POST or None, instance=instance)
    
    title = f"Edit {item_type}" if instance else f"Add {item_type}"
    redir_name = f"show_{item_type}"
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{item_type.capitalize()} added successfully!")
        return redirect(f"main:{redir_name}")
    
    return render(request, "base_create.html", MY_INFO | {
        "form": form,
        "title": title
    }) # i will fix the redirect later zzz

### ok so this one will handle ALL the cruds request, i hope its general enough but we'll see 
### its really really messy rn but i'll clean it later, in like a year or two LOL
### item_type: experience | education | projects
### update with `?id=somethingidk`

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def api_view(request, item_type):
    Model, FormClass = get_model_form(item_type)
    
    if request.method == "GET":
        items = Model.objects.all()
        
        return JsonResponse({
            "items": [{
                "id": str(obj.id),
                **{f.name: str(getattr(obj, f.name)) for f in Model._meta.fields if f.name != "id"}
            } for obj in items]
        })
    
    if request.method == "POST":
        form = FormClass(request.POST)
        
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"id": str(obj.id), "success": True}, status=201)
        
        return JsonResponse({"errors": form.errors}, status=400)

    ##
    _pk = request.GET.get("id")
    if not _pk:
        return JsonResponse({"error": "id required"}, status=400)
    
    obj = get_object_or_404(Model, id=_pk)
    ##
    
    if request.method == "PUT":
        form = FormClass(request.POST, instance=obj)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        
        return JsonResponse({"errors": form.errors}, status=400)

    # i love django man
    # if request.method == "DELETE":
    #     obj.delete()
    #     return JsonResponse({"success": True})
