from django.urls import path

from main.api import views

app_name = "api"

urlpatterns = [
    path("projects/", views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", views.project_star, name="project-star"),
]
