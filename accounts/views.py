from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # saves user and creates profile with batch
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Prevent admin/staff login from frontend
            # if user.is_staff or user.is_superuser:
            #     messages.error(request, 'Admin users must login from the admin panel.')
            #     return redirect('accounts:login')
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


# Profile view
@login_required
def profile_view(request):
    # return render(request, 'accounts/profile.html')
    profile = Profile.objects.filter(user=request.user).first()  # or get()
    return render(request, 'accounts/profile.html', {'profile': profile})



# Edit profile view (handle User and Profile forms)
@login_required
def edit_profile(request):
    profile = request.user.profile  # Fetch profile object
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'form': form,
        'profile_form': profile_form
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This deletes user and cascades to Profile
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to your homepage or login page
    return render(request, 'accounts/confirm_delete.html')