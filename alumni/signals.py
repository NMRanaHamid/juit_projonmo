from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Alumni

@receiver(post_save, sender=User)
def create_or_update_user_alumni(sender, instance, created, **kwargs):
    if created:
        Alumni.objects.create(user=instance)
    else:
        instance.alumni.save()
