from django.urls import path

from main.views import (
    api_view,
    delete_item,
    form_view,
    login_user,
    logout_user,
    register,
    show_list,
    show_main,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_list, {"item_type": "experience"}, name="show_experience"),
    path("education/",  show_list, {"item_type": "education"},  name="show_education"),
    path("projects/",   show_list, {"item_type": "projects"},   name="show_projects"),

    path("experience/create/", form_view, {"item_type": "experience"}, name="create_experience"),
    path("education/create/",  form_view, {"item_type": "education"},  name="create_education"),
    path("projects/create/",   form_view, {"item_type": "projects"},   name="create_project"),

    path("experience/delete/", delete_item, {"item_type": "experience"}, name="delete_experience"),
    path("education/delete/",  delete_item, {"item_type": "education"},  name="delete_education"),
    path("projects/delete/",   delete_item, {"item_type": "projects"},   name="delete_project"),

    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    path("api/experience/", api_view, {"item_type": "experience"}, name="api_experience"),
    path("api/education/",  api_view, {"item_type": "education"},  name="api_education"),
    path("api/projects/",   api_view, {"item_type": "projects"},   name="api_projects"),

    path("super/register/", register,    name="register"),
    path("super/login/",    login_user,  name="login"),
    path("super/logout/",   logout_user, name="logout"),
]
