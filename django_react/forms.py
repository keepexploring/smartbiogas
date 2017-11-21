from django.contrib.auth.forms import AuthenticationForm
from django import forms



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

    def confirm_login_allowed(self, user):
        if not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')