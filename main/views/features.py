from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from main.models import Project

@login_required(login_url="/super/login/")
@require_http_methods(["POST"])
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")
