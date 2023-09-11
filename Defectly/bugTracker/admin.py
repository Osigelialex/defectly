from django.contrib import admin
from .models import Project, Teams, Bugs, Comments

# Register your models here.
admin.site.register(Project)
admin.site.register(Teams)
admin.site.register(Bugs)
admin.site.register(Comments)