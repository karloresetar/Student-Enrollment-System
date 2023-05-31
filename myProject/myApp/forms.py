from django.forms import ChoiceField, ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ['username','first_name','last_name','email','role','status','password1','password2']

class UserFormEdit(ModelForm):
    class Meta:
        model = Korisnik
        fields = ['first_name', 'last_name', 'email', 'role', 'status']


class PredmetiForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['nositelj','name','kod','program','ects','sem_red','sem_izv','izborni']


    def __init__(self, *args, **kwargs):
        super(PredmetiForm, self).__init__(*args, **kwargs)
        roles = Uloge.objects.get(role='profesor')
        profesori = Korisnik.objects.filter(role=roles)
        self.fields['nositelj'].queryset = profesori