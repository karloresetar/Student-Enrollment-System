from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

# Add section -----
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

@login_required(login_url='login')
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
    
# Add section -----

#Subject section -----
@login_required(login_url='login')
def subjectlist(request):
    predmeti = Predmeti.objects.all()
    return render(request,'subject_list.html',{'predmeti':predmeti})

@login_required(login_url='login')
def subjectdetails(request, id):
    predmet = Predmeti.objects.get(id=id)
    korisnik = predmet.nositelj  # Za ispisivanje usera tj imena i prezimena profesora
    return render(request, "subject_details.html", {'predmet': predmet, 'korisnik': korisnik})

@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
def students_subject(request,predmet_id):
    predmet=Predmeti.objects.get(id = predmet_id)
    upis = Upisi.objects.filter(subject=predmet)
    return render(request, "students_subject.html", {'upisani': upis, "predmet": predmet})


@login_required(login_url='login')
def profesorsubjects(request, profesor_id):
    predmeti = Predmeti.objects.filter(nositelj = profesor_id)
    profesor = Korisnik.objects.get(id = profesor_id)
    return render(request, "profesor_subjects.html", {'predmeti': predmeti, 'profesor': profesor})


# Nositelj
@login_required(login_url='login')
def addSubjectHolder(request, id):
    predmet = get_object_or_404(Predmeti, id=id)
    roles = Uloge.objects.get(role='profesor')
    profesori = Korisnik.objects.filter(role=roles)
    selected_professor = predmet.nositelj

    if request.method == 'GET':
        data = {
            'predmet': predmet,
            'profesori': profesori,
            'selected_professor': selected_professor
        }
        return render(request, 'add_subject_holder.html', data)

    elif request.method == 'POST':
        nositelj = request.POST['profesor']
        if nositelj == '----':
            return redirect('subjectlist')
        nositeljUser = Korisnik.objects.filter(id=nositelj).first()
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

#Subject section -----


#Student, professor (User) section -----
@login_required(login_url='login')
def studentlist(request):
    users = Korisnik.objects.all()
    students = users.filter(role__role='student')
    return render(request, "student_list.html", {'users': users, 'students': students})
            

@login_required(login_url='login')
def profesorlist(request):
    users = Korisnik.objects.all()
    professors = users.filter(role__role='profesor')
    return render(request,'profesor_list.html',{'users':users,'professors':professors})


@login_required(login_url='login')
def edituser(request, id):
    user = Korisnik.objects.get(id=id)
    form = UserFormEdit(instance=user)

    if request.method == 'POST':
        form = UserFormEdit(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User edited successfully!')

            user_role = user.role.role  # Dohvacanje vrijednosti role iz objekta Uloge

            if user_role == 'student':
                return redirect('studentlist')
            elif user_role == 'profesor':
                return redirect('profesorlist')
        else:
            messages.error(request, 'Error, user could not be edited')

    return render(request, "edit_user.html", {'form': form})



@login_required(login_url='login')
def deleteuser(request, id):
    user = Korisnik.objects.get(id=id)
    if request.method == 'POST':
        if 'yes' in request.POST:
            user.delete()
            messages.success(request, 'User deleted successfully!')
            user_role = user.role.role 

            if user_role == 'student':
                return redirect('studentlist')
            elif user_role == 'profesor':
                return redirect('profesorlist')
        else:
            messages.error(request, 'Error, user could not be deleted')
    return render(request, "delete_user.html", {'user': user})



#Student, professor (Users) section -----


#Upisni CRUD section -----
def createupis(student_id, predmet_id, status):
    student = Korisnik.objects.get(id=student_id)
    predmet = Predmeti.objects.get(id=predmet_id)
    
    if Upisi.objects.filter(student=student, subject=predmet).exists():
        return
    
    Upisi.objects.create(student=student, subject=predmet, status=status)



def deleteupis(student_id,predmet_id):
    upis = Upisi.objects.filter(student = student_id, subject = predmet_id)
    upis.delete()


@login_required(login_url='login')
def upisni(request,student_id):
    predmeti = Predmeti.objects.all()
    student = Korisnik.objects.get(id = student_id)
    upisni = Upisi.objects.filter(student = student.id)
    upisani = upisni.values_list('subject', flat=True)

    if request.method =='POST':
        status = request.POST['status']
        predmet_id = request.POST['predmet_id']
        if(status == 'upisan'):
            createupis(student_id,predmet_id,status)
        elif(status == 'ispis'):
            deleteupis(student_id,predmet_id)

        
    data = {
        "predmeti": predmeti,
        "student": student,
        "upisani": upisani,
        "upisni":upisni
    }
    
    return render(request,"upisni_list.html",data)




def updateupis(student_id,predmet_id,status):
    upis = Upisi.objects.get(student=student_id, subject=predmet_id)
    upis.status = status
    upis.save()


@login_required(login_url='login')
def studentlistsubject(request,predmet_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    upis = Upisi.objects.filter(subject=predmet)

    if request.method == 'POST':
        status = request.POST['status']
        student_id = request.POST['student_id']
        updateupis(student_id,predmet_id,status)

    return render(request,"student_list_subject.html", {'upisani':upis, 'predmet':predmet})


#Upisni CRUD section -----

