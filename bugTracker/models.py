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


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    bug = models.ForeignKey(
        Bugs, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"{self.comment}"
