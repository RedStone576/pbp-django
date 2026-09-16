from django.urls import path

from main.views import show_main, show_list, form_view, api_view

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    path("experience/", show_list, {"item_type": "experience"}, name="show_experience"),
    path("education/",  show_list, {"item_type": "education"},  name="show_education"),
    path("projects/",   show_list, {"item_type": "projects"},   name="show_projects"),
    
    path("experience/create/", form_view, {"item_type": "experience"}, name="create_experience"),
    path("education/create/",  form_view, {"item_type": "education"},  name="create_education"),
    path("projects/create/",   form_view, {"item_type": "projects"},   name="create_project"),
    
    path("api/experience/", api_view, {"item_type": "experience"}),
    path("api/education/",  api_view, {"item_type": "education"}),
    path("api/projects/",   api_view, {"item_type": "projects"}),
]
