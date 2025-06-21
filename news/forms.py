from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'content': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows':5}),
        }
