from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput
from django import forms
from typing import Any
from .models import *


class CustomUserCreationForm(UserCreationForm):
    USER_TYPES=(
        ('user','User'),
        ('mechanic','Mechanic'),
        
    )
    user_type=forms.ChoiceField(choices=USER_TYPES,)

    class Meta:
        model=CustomeUser
        fields = ( 'username','password1','password2','user_type')        
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "title": "Your name",
                "placeholder": "Enter your name"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "title": "Your name",
                "placeholder": "Enter your password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm your password"
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user',)
        widgets={
            "dob":forms.DateInput(attrs={"type":"date"}),
            # 'profile_pic': ClearableFileInput(attrs={'clear_label': ''}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['profile_pic'].widget.attrs.pop('initial_text', None)
    #     self.fields['profile_pic'].widget.attrs.pop('clear_checkbox_label', None)
    
class MecProfileForm(forms.ModelForm):
    class Meta:
        model=MechanicProfile
        exclude=('user','is_approved','is_active','average_rating',)
        widgets={
            "dob":forms.DateInput(attrs={"type":"date"}),
            # 'profile_pic': ClearableFileInput(attrs={'clear_label': ''}),
        }
        
class AdminCreationForm(UserCreationForm):
    USER_TYPES=(
        ('administrator','admin'),
        ('user','User'),
        ('mechanic','Mechanic'),        
    )
    user_type=forms.ChoiceField(choices=USER_TYPES,)

    class Meta:
        model=CustomeUser
        fields = ( 'username','password1','password2','user_type')        
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "title": "Your name",
                "placeholder": "Enter the name"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "title": "Your name",
                "placeholder": "Enter the password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm the password"
            }),
        }
