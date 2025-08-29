from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    batch = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile.batch = self.cleaned_data.get('batch')
        if commit:
            user.profile.save()
        return user

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# Edit Profile info (including batch)
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'batch', 'linkedin', 'facebook']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'w-full border p-2 rounded'}),
            'bio': forms.Textarea(attrs={'class': 'w-full border p-2 rounded', 'rows': 3}),
            'batch': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'linkedin': forms.URLInput(attrs={'class': 'w-full border p-2 rounded', 'placeholder': 'LinkedIn Profile URL'}),
            'facebook': forms.URLInput(attrs={'class': 'w-full border p-2 rounded', 'placeholder': 'Facebook Profile URL'}),
        }
