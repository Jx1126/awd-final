from django import forms
from .models import AppUser, UserStatusUpdate
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserProfileForm(forms.ModelForm):
    user_role_radio = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )
    user_role = forms.ChoiceField(choices=user_role_radio, widget=forms.RadioSelect)

    class Meta:
        model = AppUser
        fields = ("real_name", "user_role", "bio")


class UserStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = UserStatusUpdate
        fields = ["status_title", "status_content"]


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["real_name", "bio", "profile_photo"]
