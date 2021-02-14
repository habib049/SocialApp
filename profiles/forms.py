from .models import UserProfile
from accounts.models import User
from django import forms


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(UserUpdateForm):
    class Meta:
        model = UserProfile
