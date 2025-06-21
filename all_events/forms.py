from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date' ,'location','start_time','end_time', ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full border border-gray-300 p-2 rounded'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full border border-gray-300 p-2 rounded'
            }) ,

        }
