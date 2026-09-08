from django.contrib import admin
from django.urls import path, include

from porto.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),

]
