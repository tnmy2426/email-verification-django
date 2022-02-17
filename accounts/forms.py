from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile

class RegisterForm(UserCreationForm):
    #To show only 1 password for registration, uncomment the line  del self.fields['password2'] and remove password2 in this file and register.html
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #del self.fields['password2']


    username = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'email'
            }
    ))
    
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'id': 'password1',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'id': 'password2',
        }
    ))

    # This is used as a field to write into the DB. Hidden field in the form
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '', 
            'id': 'email'
            }
    ))
    
    class Meta:
        model=User
        fields=['username','password1','password2','email']

 
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'email'}))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ))



class ProfileForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput)
    
    class Meta:
        model=Profile
        fields=('image','First_Name','Last_Name')