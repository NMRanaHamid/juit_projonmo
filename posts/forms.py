from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'content': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':2, 'class':'border rounded p-2 w-full', 'placeholder':'Write a comment...'})
        }
