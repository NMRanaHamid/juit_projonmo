from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,default='avatars/default_avatar.jpg')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    batch = models.CharField(max_length=50, blank=True)

    linkedin = models.URLField(max_length=255,blank=True, null=True)
    facebook = models.URLField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.username
