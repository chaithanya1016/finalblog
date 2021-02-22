from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from webapp.models import Article,Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'location', 'birth_date')

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-group col-md-4'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control form-group col-md-4'}))
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']
        labels = {'username': 'User Name', 'first_name' : 'First Name', 'last_name' : 'Last Name', 'email': 'Email'} 
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-group col-md-4'}), 
            'first_name': forms.TextInput(attrs={'class':'form-control form-group col-md-4'}), 
            'last_name': forms.TextInput(attrs={'class':'form-control form-group col-md-4'}), 
            'email': forms.TextInput(attrs={'class':'form-control form-group col-md-4'}), 
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control form-group col-md-4'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': True, 'class': 'form-control form-group col-md-4'}))

