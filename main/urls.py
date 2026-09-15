from django.urls import path

from main.views import \
show_main, \
show_experience, show_education, show_projects, \
create_experience, create_education, create_projects

app_name = "main"

urlpatterns = [
    path("",            show_main,        name="show_main"),
    path("experience/", show_experience,  name="show_experience"),
    path("education/",  show_education,   name="show_education"),
    path("projects/",   show_projects,    name="show_projects"),
    
    path("experience/create/", create_experience, name="create_experience"),
    path("education/create/",  create_education,  name="create_education"),
    path("projects/create/",   create_projects,   name="create_project"),
    
]
