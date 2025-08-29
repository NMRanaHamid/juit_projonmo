
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.home,name='home') ,
    path('notifications/', include('notifications.urls')),
    path('accounts/', include('accounts.urls')),  # Home/login
    path('__reload__',include('django_browser_reload.urls')) ,
    path('admin/', admin.site.urls),
    path('alumni/', include('alumni.urls')),
    path('events/', include('all_events.urls')),
    path('news/', include('news.urls')),
    path('posts/', include('posts.urls')),
    path('jobs/', include('jobs.urls')),
    path('contact/', include('contact.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
