from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    # path('register/login/', views.login_view, name='log_in'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
]
