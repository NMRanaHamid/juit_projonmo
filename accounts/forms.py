from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# --- Registration Form ---
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    batch = forms.CharField(required=True)  # Batch field from Profile

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        batch = self.cleaned_data.get('batch')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.batch = batch
        profile.save()
        return user

# --- User Edit Form ---
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    batch = forms.CharField(required=True, max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['batch'].initial = self.instance.profile.batch

    def save(self, commit=True):
        user = super().save(commit)
        batch = self.cleaned_data.get('batch')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.batch = batch
        if commit:
            profile.save()
        return user

# --- Profile Edit Form (With Tailwind Styling + No Clear Checkbox) ---
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'batch']

        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded',
                'rows': 3,
            }),
            'batch': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded',
            }),
        }
