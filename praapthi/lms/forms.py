
from django.contrib.auth.models import User

from .models import UserProfile

from django import forms

from django.forms import ModelForm, Textarea, TextInput, Select, PasswordInput

"""
TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),('O', 'Others'),)
COUNTRY_CHOICES = (('India', 'India'), ('Pakistan', 'Pakistan'), ('Others', 'Others'),)

class UserForm(forms.ModelForm):
	docstring for RegisterForm
	class Meta:
		model = User
		fields = ["first_name", "last_name", "email", "username", "password"]
		widgets = {
        	'first_name': TextInput(attrs={'class' : 'form-control'}),
        	'last_name': TextInput(attrs={'class' : 'form-control'}),
        	'email': TextInput(attrs={'class' : 'form-control'}),
        	'username': TextInput(attrs={'class' : 'form-control'}),
        	'password': PasswordInput(attrs={'class' : 'form-control'}),
        }



class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ["country", "gender", "conditions", "profile_image",]
		widgets = {
        	'country': Select(attrs={'class' : 'form-control'}, choices=COUNTRY_CHOICES),
        	'gender': Select(attrs={'class' : 'form-control'}, choices=GENDER_CHOICES),
        	'conditions': forms.TextInput(attrs={'class' : 'form-control'}),
        	'profile_image': TextInput(attrs={'class' : 'form-control'}),
        	}

"""


"""
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
        	'username': TextInput(attrs={'class' : 'formelement'}),
        }
"""

"""class UserProfileForm(forms.ModelForm):
        class Meta:
                model = UserProfile
                fields = ['website', 'picture']"""
