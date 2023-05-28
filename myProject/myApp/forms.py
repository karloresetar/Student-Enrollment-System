from django.forms import ChoiceField, ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ['username','first_name','last_name','email','role','status','password1','password2']