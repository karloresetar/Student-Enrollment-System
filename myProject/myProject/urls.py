"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myApp import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('adduser/',views.adduser, name='adduser'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('addsubject/', views.addsubject, name='addsubject'),
    path('addsubholder/<int:id>/', views.addSubjectHolder, name='addsubholder'),
    path('subjectlist/', views.subjectlist, name='subjectlist'),
    path('subjectdetails/<int:id>', views.subjectdetails, name='subjectdetails'),
    path('editsubject/<int:id>', views.editsubject, name='editsubject'),
    path('deletesubject/<int:id>', views.deletesubject, name='deletesubject'),
    path('studentsubject/<int:predmet_id>/', views.students_subject, name='students_subject'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('profesorlist/', views.profesorlist, name='profesorlist'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
    path('profesorsubjects/<int:profesor_id>', views.profesorsubjects, name='profesorsubjects'),
    path('studentlistsubject/<int:predmet_id>/', views.studentlistsubject, name='studentlistsubject'),
    path('upisni/<int:student_id>/', views.upisni, name='upisni'),
]

urlpatterns += staticfiles_urlpatterns()