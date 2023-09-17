from django.contrib import admin
from .models import Project, Bugs, Comments


admin.site.register(Project)
admin.site.register(Bugs)
admin.site.register(Comments)