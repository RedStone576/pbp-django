from django.urls import path

from main.views import (
    login_user,
    logout_user,
    register,
    show_list,
    show_main,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_list, {"item_type": "experience"}, name="show_experience"),
    path("education/",  show_list, {"item_type": "education"},  name="show_education"),
    path("projects/",   show_list, {"item_type": "projects"},   name="show_projects"),

    path("super/register/", register,    name="register"),
    path("super/login/",    login_user,  name="login"),
    path("super/logout/",   logout_user, name="logout"),
]
