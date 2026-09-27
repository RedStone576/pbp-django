from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

import json
import requests
import datetime

# nice read: https://docs.djangoproject.com/en/5.0/_modules/django/views/decorators/http/#require_http_methods

from main.models import Experience, Education, Project
from main.forms import ExperienceForm, EducationForm, ProjectForm

def MY_INFO(request):
    return {
        "name": "Ilham Firmansyah", 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        "role": "Insinyur Perangkat Lunak",
        "last_login": request.COOKIES.get("last_login", "No active login session / Cookie not found")
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
    
    return render(request, "index.html", MY_INFO(request) | context)

###

def show_list(request, item_type):
    api_url = f"{request.scheme}://{request.get_host()}/api/{item_type}/"
    
    try:
        response = requests.get(api_url, cookies=request.COOKIES, timeout=10)
        response.raise_for_status()
        
        raw_json = response.json()
        
        if isinstance(raw_json, str):
            items = json.loads(raw_json)
        else:
            items = raw_json
        
        parsed_items = []
        for item in items:
            fields = item["fields"]
            if "starred_by" in fields:
                fields["starred_by"] = [x[0] for x in fields["starred_by"]]
            parsed_items.append({"id": item["pk"], **fields})
        
    except requests.RequestException as e:
        print(f"Error: {e}")
        parsed_items = []
        
    context = {f"{item_type}_list": parsed_items}
    return render(request, f"{item_type}.html", MY_INFO(request) | context)

###

@login_required(login_url="/super/login/")
def form_view(request, item_type):
    if not request.user.is_superuser:
        raise PermissionDenied

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
    
    return render(request, "base_create.html", MY_INFO(request) | {
        "form": form,
        "title": title
    }) # i will fix the redirect later zzz

# akan ada waktunya manusia akan sadar bahwa semuanya eventually jadi POST request xixixixi
@login_required(login_url="/super/login/")
def delete_item(request, item_type):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method != "POST":
        return redirect(f"main:show_{item_type}")
        
    Model, _ = get_model_form(item_type)
    _pk = request.GET.get("id")
    
    if not _pk:
        return redirect(f"main:show_{item_type}")
        
    obj = get_object_or_404(Model, id=_pk)
    obj.delete()
    
    messages.success(request, f"{item_type.capitalize()} deleted successfully!")
    
    return redirect(f"main:show_{item_type}")

### ok so this one will handle ALL the cruds request, i hope its general enough but we'll see 
### its really really messy rn but i'll clean it later, in like a year or two LOL
### item_type: experience | education | projects
### update with `?id=somethingidk`

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def api_view(request, item_type):
    Model, FormClass = get_model_form(item_type)
    
    if request.method == "GET":
        items = Model.objects.all()
        
        items_json = serializers.serialize("json", items, use_natural_foreign_keys=True)
        return HttpResponse(items_json, content_type="application/json")
    
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
    if request.method == "DELETE":
        obj.delete()
        return JsonResponse({"success": True})


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        
        return redirect("main:login")

    context = {
        "form": form,
    }

    return render(request, "register.html", MY_INFO(request) | context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        
        login(request, user)
        
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return response

    context = {
        "form": form,
    }

    return render(request, "login.html", MY_INFO(request) | context)

def logout_user(request):
    logout(request)
    
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    
    return response

@login_required(login_url="/super/login/")
@require_http_methods(["POST"])
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")
