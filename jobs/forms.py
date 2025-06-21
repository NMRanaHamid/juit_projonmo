from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'description', 'requirements', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':4}),
            'requirements': forms.Textarea(attrs={'rows':3}),
        }
