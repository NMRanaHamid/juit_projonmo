from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded p-2 w-full'}),
            'subject': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'message': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 5}),
        }
