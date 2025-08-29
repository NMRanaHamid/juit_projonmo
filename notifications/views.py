from django.shortcuts import render
from .models import Notification
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

def all_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    else:
        notifications = []
    return render(request, 'notifications/all_notifications.html', {'notifications': notifications})

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return JsonResponse({'success': True})