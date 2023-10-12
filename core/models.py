from django.db import models
from django.contrib.auth.models import User
from bugs.models import Bugs


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    bug = models.ForeignKey(
        Bugs, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"{self.comment}"
