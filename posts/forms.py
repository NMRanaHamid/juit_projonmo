from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'content': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 6}),
        }
