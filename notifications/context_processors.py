from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = notifications.filter(read=False).count()  # Filter first
        latest_notifications = notifications[:20]  # Slice after filtering
        return {
            'notifications': latest_notifications,
            'unread_count': unread_count
        }
    return {}
