from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
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


def addsubject(request):
    message = None
    if request.method == 'GET':
        form = PredmetiForm()
    elif request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Subject created successfully'
            return redirect('subjectlist')
        else:
            message = 'Error, subject could not be created'
    
    return render(request,'add_subject.html',{'form':form,'message':message})

def addSubjectHolder(request, id):
    predmet = get_object_or_404(Predmeti, id=id)
    roles = Uloge.objects.get(role='profesor')
    profesori = Korisnik.objects.filter(role=roles)

    if request.method == 'GET':
        data = {
            'predmet': predmet,
            'profesori': profesori
        }
        return render(request, 'add_subject_holder.html', data)

    elif request.method == 'POST':
        nositelj = request.POST['profesor']
        if nositelj == '----':
            return redirect('subjectlist')
        nositeljUser = Korisnik.objects.filter(username=nositelj).first()
        if nositeljUser:
            predmet.nositelj = nositeljUser
            predmet.save()
            messages.success(request, 'Subject holder updated successfully!')
        else:
            messages.error(request, 'Error: Invalid subject holder')
        return redirect('subjectlist')

    else:
        messages.error(request, 'Something went wrong')
        return redirect('subjectlist')
    

def subjectlist(request):
    predmeti = Predmeti.objects.all()
    return render(request,'subject_list.html',{'predmeti':predmeti})

def subjectdetails(request, id):
    predmet = Predmeti.objects.get(id=id)
    korisnik = predmet.nositelj  # Za ispisivanje usera tj imena i prezimena profesora
    return render(request, "subject_details.html", {'predmet': predmet, 'korisnik': korisnik})


def editsubject(request, id):
    predmet = Predmeti.objects.get(id=id)
    form = PredmetiForm(instance=predmet)

    if request.method == 'POST':
        form = PredmetiForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject edited successfully!')
            return redirect('subjectlist')
        else:
            messages.error(request, 'Error, subject could not be edited')

    return render(request, "edit_subject.html", {'form': form})


def deletesubject(request, id):
    predmet = Predmeti.objects.get(id=id)
    if request.method == 'POST':
        if 'yes' in request.POST:
            predmet.delete()
            messages.success(request, 'Subject deleted successfully!')
            return redirect('subjectlist')
        else:
            return redirect('subjectlist')
    return render(request, "delete_subject.html", {'subject': predmet})


def students_subject(request,predmet_id):
    predmet=Predmeti.objects.get(id = predmet_id)
    upis = Upisi.objects.filter(subject=predmet)
    return render(request, "students_subject.html", {'upisani': upis, "predmet": predmet})
            


