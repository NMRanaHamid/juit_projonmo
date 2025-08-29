from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event, EventRegistration
from .forms import EventForm

def is_admin(user):
    return user.is_staff or user.is_superuser


def event_list(request):
    events = Event.objects.all().order_by('-event_date')
    return render(request, 'all_events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Check if the current user is registered
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    return render(request, 'all_events/event_detail.html', {'event': event, 'is_registered': is_registered})


@login_required
@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('all_events:event_list')
    else:
        form = EventForm()
    return render(request, 'all_events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(is_admin)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('all_events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'all_events/event_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('all_events:event_list')
    return render(request, 'all_events/event_confirm_delete.html', {'event': event})


# ---------------- New Features ---------------- #

# Event Registration
@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        return redirect('all_events:event_detail', pk=event.pk)

    if request.method == 'POST':
        EventRegistration.objects.create(event=event, user=request.user)
        return redirect('all_events:event_detail', pk=event.pk)

    return render(request, 'all_events/event_register.html', {'event': event})


# Registered Users List (Admin only)
@staff_member_required
def event_registered_users(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = EventRegistration.objects.filter(event=event).select_related('user', 'user__profile').order_by('user__profile__batch')
    return render(request, 'all_events/event_registered_users.html', {
        'event': event,
        'registrations': registrations
    })
