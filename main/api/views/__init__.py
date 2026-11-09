from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.api.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.api.serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
)
from main.models import Education, Experience, Project

RESOURCES = {
    "education": {
        "model": Education,
        "serializer": EducationSerializer,
        "search_field": "program",
        "ordering": ("institution", "id"),
    },
    "experience": {
        "model": Experience,
        "serializer": ExperienceSerializer,
        "search_field": "title",
        "ordering": ("title", "id"),
    },
    "projects": {
        "model": Project,
        "serializer": ProjectSerializer,
        "search_field": "title",
        "ordering": ("title", "id"),
    },
}


def get_resource(name):
    try:
        return RESOURCES[name]
    except KeyError as error:
        raise Http404 from error


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def list_view(request, resource):
    config = get_resource(resource)

    if request.method in ("GET", "HEAD"):
        items = config["model"].objects.prefetch_related("starred_by")
        query = request.query_params.get("title", "").strip()
        if query:
            items = items.filter(**{f"{config['search_field']}__icontains": query})
        items = items.order_by(*config["ordering"])
        serializer = config["serializer"](
            items, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = config["serializer"](data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def detail_view(request, resource, item_id):
    config = get_resource(resource)
    item = get_object_or_404(
        config["model"].objects.prefetch_related("starred_by"), pk=item_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = config["serializer"](item, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = config["serializer"](
        item,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def star_view(request, resource, item_id):
    config = get_resource(resource)
    item = get_object_or_404(config["model"], pk=item_id)
    stars = item.starred_by

    if stars.filter(pk=request.user.pk).exists():
        stars.remove(request.user)
    else:
        stars.add(request.user)

    serializer = config["serializer"](item, context={"request": request})
    return Response(serializer.data)
