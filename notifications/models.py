from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIF_TYPES = (
        ('job', 'Job'),
        ('event', 'Event'),
        ('post', 'Post'),
        ('news', 'News'),
        ('general', 'General'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='general')
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    url = models.CharField(max_length=500, blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
