from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import *
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=50, min_length=11, widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'display_name', 'bio', 'image']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=200,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Enter your current password'}))
    password1 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password'}))
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password'}))

    # def clean_current_password(self):
    #     current_password = self.cleaned_data.get('current')
    #     email = self.cleaned_data.get('user-email')
    #     user = User.objects.filter(email=email, password=current_password)
    #     if user.exists():
    #         return current_password
    #     raise ValidationError("Please enter your password correctly", code="current_password_wrong")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords are not the same..', code='not_same_password')
        return password1
