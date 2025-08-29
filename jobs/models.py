from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=150)
    company_url = models.URLField(max_length=250,blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(default=now)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
