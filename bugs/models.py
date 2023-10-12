from django.contrib.auth.models import User
from project.models import Project
from django.db import models


class Bugs(models.Model):
    SEVERITY_CHOICES = [
        ('high', 'High'),
        ('mid', 'Mid'),
        ('low', 'Low')
    ]
    title = models.CharField(max_length=75)
    description = models.TextField()
    severity = models.CharField(
        max_length=10, choices=SEVERITY_CHOICES, default='mid')
    open = models.BooleanField(default=True)
    assignees = models.ManyToManyField(User, related_name='assigned')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='bugs')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bugs')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='resolved_bugs', null=True)

    def __str__(self) -> str:
        return f"{self.title}"