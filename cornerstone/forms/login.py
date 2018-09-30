from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth. models import User
from captcha.fields import CaptchaField


class StaffForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput)
    captcha = CaptchaField()


class ReportForm(forms.Form):
    starttime = forms.CharField(max_length=64)
    endtime = forms.CharField(max_length=64)
