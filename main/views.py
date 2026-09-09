from django.shortcuts import render

from main.models import Experience, Education, Project

MY_NAME = "Ilham Firmansyah"

def show_main(request):
    # mkay context.name are more like title or something bruh
    context = {
        "name": MY_NAME, 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "bio": (
            "Recreational programmer, linguistic enthusiast, supposedly computer philosopher, and Tetris player at heart."
            "<br><br>Loves raw JavaScript at its finest. TypeScript too, if you insist."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": MY_NAME,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": MY_NAME,
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def show_projects(request):
    context = {
        "name": MY_NAME,
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
