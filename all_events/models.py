from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField(default=None)
    location = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,default=None)


    def __str__(self):
        return self.title
