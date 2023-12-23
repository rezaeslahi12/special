from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control' , 'placeholder':'Your Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control' , 'placeholder' : 'Your Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control' , 'placeholder':'Your Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control' , 'placeholder':'Your Password'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username)
        if user:
            raise ValidationError('This user already exists')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Password must be Match')
class UserLoginForm(forms.Form):
    username = forms.CharField(label='Enter your username or email',widget=forms.TextInput(attrs = {'class':'form-control' , 'placeholder':'Enter Username Or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control' , 'placeholder':'Your Password'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age','bio')