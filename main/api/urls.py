from django.urls import path

from main.api import views

app_name = "api"

urlpatterns = [
    path("projects/",                     views.list_view,   {"resource": "projects"}, name="project-list"),
    path("projects/<uuid:item_id>/",      views.detail_view, {"resource": "projects"}, name="project-detail"),
    path("projects/<uuid:item_id>/star/", views.star_view,   {"resource": "projects"}, name="project-star"),

    path("education/",                     views.list_view,   {"resource": "education"}, name="education-list"),
    path("education/<uuid:item_id>/",      views.detail_view, {"resource": "education"}, name="education-detail"),
    path("education/<uuid:item_id>/star/", views.star_view,   {"resource": "education"}, name="education-star"),

    path("experience/",                     views.list_view,   {"resource": "experience"}, name="experience-list"),
    path("experience/<uuid:item_id>/",      views.detail_view, {"resource": "experience"}, name="experience-detail"),
    path("experience/<uuid:item_id>/star/", views.star_view,   {"resource": "experience"}, name="experience-star"),
]
