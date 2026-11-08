from django.urls import path

from main.api import views

app_name = "api"

urlpatterns = [
    path("projects/",                        views.project_list,   name="project-list"),
    path("projects/<uuid:project_id>/",      views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", views.project_star,   name="project-star"),
    
    path("education/",                          views.education_list,   name="education-list"),
    path("education/<uuid:education_id>/",      views.education_detail, name="education-detail"),
    path("education/<uuid:education_id>/star/", views.education_star,   name="education-star"),

    path("experience/",                           views.experience_list,   name="experience-list"),
    path("experience/<uuid:experience_id>/",      views.experience_detail, name="experience-detail"),
    path("experience/<uuid:experience_id>/star/", views.experience_star,   name="experience-star"),
]
