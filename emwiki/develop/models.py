from django.db import models
from django.conf import settings


class Develop(models.Model):
    github_id = models.CharField(max_length=100, default='', blank=True)
    repository_name = models.CharField(max_length=100, default='', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username}, {self.github_id}"
