from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import Job
from all_events.models import Event
from posts.models import Post
from news.models import News
from .models import Notification

def create_notification(instance, notif_type, title=None, url=None):
    user = getattr(instance, 'posted_by', None) or getattr(instance, 'author', None)
    title = title or getattr(instance, 'title', '')
    url = url or f"/{notif_type}/{instance.pk}/"

    # Prevent duplicate notifications for the same instance
    if not Notification.objects.filter(user=user, notif_type=notif_type, title=title, url=url).exists():
        Notification.objects.create(
            user=user,
            notif_type=notif_type,
            title=title,
            message=f"New {notif_type} created: {title}",
            url=url
        )

# Jobs
@receiver(post_save, sender=Job)
def job_created(sender, instance, created, **kwargs):
    if created:
        create_notification(instance, 'job', title=instance.title, url=f"/jobs/job/{instance.id}/")

# Events
@receiver(post_save, sender=Event)
def event_created(sender, instance, created, **kwargs):
    if created:
        create_notification(instance, 'event', title=instance.title, url=f"/events/{instance.id}/")

# Posts
@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        create_notification(instance, 'post', title=instance.title, url=f"/posts/{instance.id}/")

# News
@receiver(post_save, sender=News)
def news_created(sender, instance, created, **kwargs):
    if created:
        create_notification(instance, 'news', title=instance.title, url=f"/news/{instance.id}/")
