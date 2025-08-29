from django.shortcuts import render
from all_events.models import Event

# app_name = 'templates'

def home(request) :
    gallery_image = [
        'images/football1.jpeg', 
        'images/football2.jpeg',
        'images/saint.jpeg', 
        'images/bus.jpg', 
        'images/basket.jpeg',
        'images/basket2.jpg'
        
    ]
    alumni_image = [
        {
            'image':'images/mir.jpg',
            'name': 'Mir Noshin Jahan',
            'designation': 'Software Engineer at Google'
        },
        {
            'image':'images/milon.jpg',
            'name': 'Faruk Hossain Milon',
            'designation': 'Software Engineer at Amazon'
        },
        {
            'image':'images/asif.jpg',
            'name': 'Asif Julfikar Shoumik',
            'designation': 'Software Engineer at Meta'
        },
        {
            'image':'images/sohel.jpg',
            'name': 'Sahedul Islam Sohel',
            'designation': 'Software Engineer at Google'
        },
        
    ]
    upcoming_events = Event.objects.order_by('event_date')[:3]
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(read=False).count()
        notifications = request.user.notifications.order_by('-created_at')
        # mark all as read
        notifications.update(read=True)
    else:
        unread_count = 0
        notifications = []  # or Notification.objects.none() if you want a queryset

    return render(
        request,
        'home.html',
        {
            'gallery_images': gallery_image,
            'alumni_images': alumni_image,
            'upcoming_events': upcoming_events,
            'unread_count': unread_count,
            'notifications': notifications,  # send to template if needed
        }
    )
