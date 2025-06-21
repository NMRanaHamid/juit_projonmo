from django.db import models
from django.contrib.auth.models import User

class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    graduation_year = models.CharField(max_length=50, blank=True, null=True)
    current_position = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Alumni"
