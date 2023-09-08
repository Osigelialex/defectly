from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='projects')

    def __str__(self) -> str:
        return f"{self.name}"
    
class Teams(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    members = models.ManyToManyField(User, related_name='teams')
    projects = models.ManyToManyField(Project, related_name='teams')
    
    def __str__(self) -> str:
        return f"{self.name}"