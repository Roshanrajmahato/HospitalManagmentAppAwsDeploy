from django import forms
from django.contrib.auth.models import User
from learnapp.models import UserDetails
from django_recaptcha.fields import ReCaptchaField
from django.conf import settings

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username','email','password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone','address','street','city','state','zipcode','userpic']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only add captcha if not disabled
        if not getattr(settings, 'RECAPTCHA_DISABLED', False):
            self.fields['captcha'] = ReCaptchaField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone','address','street','city','state','zipcode','userpic']
        