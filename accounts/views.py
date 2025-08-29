from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from notifications.models import Notification

# ---------------- Registration ----------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('accounts:my_profile_redirect')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('accounts:my_profile_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# ---------------- Logout ----------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

# ---------------- Profile View ----------------
@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    avatar_url = profile.avatar.url if profile.avatar else '/static/images/default_avatar.jpg'

    # Get all notifications for the user, ordered newest first
    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Count unread notifications BEFORE slicing
    unread_count = all_notifications.filter(read=False).count()

    # Slice latest 20 for display
    notifications = all_notifications[:20]

    # Mark the sliced notifications as read (if needed)
    # Use IDs to update, not the sliced queryset
    unread_ids = [n.id for n in notifications if not n.read]
    Notification.objects.filter(id__in=unread_ids).update(read=True)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'avatar_url': avatar_url,
        'notifications': notifications,
        'unread_count': unread_count
    })

# ---------------- Redirect to own profile ----------------
@login_required
def my_profile_redirect(request):
    return redirect('accounts:profile', username=request.user.username)

# ---------------- Edit Profile ----------------
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', username=user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'form': user_form,
        'profile_form': profile_form
    })

# ---------------- Delete Account ----------------
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete.html')
