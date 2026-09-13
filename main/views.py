from django.shortcuts import render

from main.models import Experience, Education, Project

MY_NAME = "Ilham Firmansyah"

def show_main(request):
    # mkay context.name are more like title or something bruh
    context = {
        "name": MY_NAME, 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        
        "bio": (
            "<ul>"
            "<li><i>Insinyur Perangkat Lunak</i></li>"
            "<li>Recreational programmer</li>"
            "<li>linguistic enthusiast</li>"
            "<li>supposedly computer philosopher</li>"
            "<li>and Tetris player at heart.</li>"
            "</ul>"
            "Loves raw JavaScript at its finest. TypeScript too, if you insist."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": MY_NAME, 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": MY_NAME, 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def show_projects(request):
    context = {
        "name": MY_NAME, 
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
