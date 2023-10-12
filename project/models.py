from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='projects')

    def __str__(self) -> str:
        return f"{self.name}"