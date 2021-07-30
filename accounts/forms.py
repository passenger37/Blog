from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Profile

class SignUp(UserCreationForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={"placeholder":"Username","class":"signup_form_input"}))
    email=forms.CharField(label='Email',widget=forms.EmailInput(attrs={"placeholder":"Email","class":"signup_form_input"}))
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"signup_form_input"}))
    password2=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password","class":"signup_form_input"}))


class Login(AuthenticationForm):
        username=forms.CharField(error_messages={'required':"Enter Your Username  !!"},label='Username',widget=forms.TextInput(attrs={"placeholder":"Username","class":"login_form_input"}))
        password=forms.CharField(error_messages={'required':"Enter Correct Password !!"},label='Password',widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"login_form_input"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['mobile_no','profile_img','address']
