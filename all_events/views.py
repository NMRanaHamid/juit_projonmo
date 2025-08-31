from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventForm
from notifications.models import Notification

# ---------------- Helper Functions ---------------- #

def is_admin(user):
    """Check if user is staff or superuser."""
    return user.is_staff or user.is_superuser

# ---------------- Event Views ---------------- #

def event_list(request):
    """List all events ordered by latest date."""
    events = Event.objects.all().order_by('-event_date')
    return render(request, 'all_events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Redirect anonymous users to registration page
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # <- your registration URL name

    # Check if the logged-in user is registered
    is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    
    return render(request, 'all_events/event_detail.html', {
        'event': event,
        'is_registered': is_registered
    })

@login_required
@user_passes_test(is_admin)
def event_create(request):
    """Create new event (Admin only)."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            # Notify all active users about new event
            for u in User.objects.filter(is_active=True):
                Notification.objects.create(
                    user=u,
                    notif_type='event',
                    title=f"New Event: {event.title}",
                    message=f"A new event '{event.title}' has been created.",
                    url=f"/events/{event.pk}/"
                )

            messages.success(request, "Event created successfully!")
            return redirect('all_events:event_list')
    else:
        form = EventForm()
    return render(request, 'all_events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(is_admin)
def event_edit(request, pk):
    """Edit existing event (Admin only)."""
    event = get_object_or_404(Event, pk=pk)
    if not request.user.is_authenticated:
        return redirect('accounts:register') 
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('all_events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'all_events/event_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def event_delete(request, pk):
    """Delete an event (Admin only)."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('all_events:event_list')
    return render(request, 'all_events/event_confirm_delete.html', {'event': event})


# ---------------- Event Registration ---------------- #

@login_required
def event_register(request, pk):
    """Register logged-in user for an event."""
    event = get_object_or_404(Event, pk=pk)

    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "You have already registered for this event.")
        return redirect('all_events:event_detail', pk=event.pk)

    if request.method == 'POST':
        EventRegistration.objects.create(event=event, user=request.user)
        messages.success(request, "You have successfully registered for this event!")
        return redirect('all_events:event_detail', pk=event.pk)

    return render(request, 'all_events/event_register.html', {'event': event})


# ---------------- Registered Users ---------------- #

@login_required
def event_registered_users(request, pk):
    """List all users registered for an event. Visible to all users."""
    event = get_object_or_404(Event, pk=pk)
    registrations = EventRegistration.objects.filter(
        event=event
    ).select_related('user', 'user__profile').order_by('user__profile__batch')
    
    return render(request, 'all_events/event_registered_users.html', {
        'event': event,
        'registrations': registrations
    })
@login_required
def event_registered_users(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = EventRegistration.objects.filter(
        event=event
    ).select_related('user', 'user__profile').order_by('user__profile__batch')

    # Prepare grouped registrations
    grouped = {}
    special_groups = ['teacher', 'staff', 'lab assistant']

    for reg in registrations:
        batch = reg.user.profile.batch.lower()  # normalize
        if batch in special_groups:
            key = batch.title()  # Capitalize first letter: "Teacher"
        else:
            key = reg.user.profile.batch
        grouped.setdefault(key, []).append(reg)

    # Sort: special sections first in defined order, then numeric batches
    sorted_grouped = {}
    for key in ['Teacher', 'Staff', 'Lab Assistant'] + sorted(
        [k for k in grouped.keys() if k.title() not in ['Teacher', 'Staff', 'Lab Assistant']],
        key=lambda x: (int(x) if x.isdigit() else x)
    ):
        if key in grouped:
            sorted_grouped[key] = grouped[key]

    return render(request, 'all_events/event_registered_users.html', {
        'event': event,
        'grouped_registrations': sorted_grouped
    })
