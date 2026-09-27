from django.contrib import admin

# just for a while :P
from .models import Education, Experience, Project

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
