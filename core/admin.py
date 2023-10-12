from django.contrib import admin
from .models import Bugs, Comments
from project.models import Project


admin.site.register(Project)
admin.site.register(Bugs)
admin.site.register(Comments)