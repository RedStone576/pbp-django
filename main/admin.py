from django.contrib import admin

# just for a while :P
from .models import Experience, Education, Project

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
