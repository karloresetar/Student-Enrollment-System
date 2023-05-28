from django.shortcuts import render
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'home.html')

def adduser(request):
    message = None

    if request.method == 'GET':
        form = UserForm()
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'User created successfully'
            form = UserForm() #za clearenje inputa radim novu instacu forme nakon sto je submitano
        else:
            message = 'Error, user is not created successfully'

    return render(request, 'add_user.html', {'form': form, 'message': message})
