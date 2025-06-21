from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Sending email to site admin
            send_mail(
                subject=f"New Contact Message: {contact_message.subject}",
                message=f"From: {contact_message.name} <{contact_message.email}>\n\n{contact_message.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(request, "Your message was sent successfully!")
            return redirect('contact:contact')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
