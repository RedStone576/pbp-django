from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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


def show_experience(request):
    context = {
        "experience_list": Experience.objects.all(),
    }
    
    return render(request, "experience.html", MY_INFO | context)


def show_education(request):
    context = {
        "education_list": Education.objects.all(),
    }
    
    return render(request, "education.html", MY_INFO | context)


def show_projects(request):
    context = {
        "project_list": Project.objects.all(),
    }
    
    return render(request, "projects.html", MY_INFO | context)

###

def create_experience(request):
    form = ExperienceForm(request.POST or None)
 
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience added successfully!")
        return redirect("main:show_experience")
 
    context = {
        "form": form,
    }
    
    return render(request, "experience_create.html", MY_INFO | context)
 
 
def create_education(request):
    form = EducationForm(request.POST or None)
 
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education added successfully!")
        return redirect("main:show_education")
 
    context = {
        "form": form,
    }
    
    return render(request, "education_create.html", MY_INFO | context)

def create_projects(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }
    
    return render(request, "projects_create.html", MY_INFO | context)
