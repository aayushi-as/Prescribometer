from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register, name='register'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('profile/',views.profile, name='profile'),
    path('analytics/',views.analytics, name='analytics'),
    path('newPatient/',views.newPatient, name='newPatient'),
    path('existingPatient/',views.existingPatient, name='existingPatient'),
    path('newPatient/record/',views.record,name = 'record'),
    path('newPatient/record/save_changes/',views.save_changes,name = 'save_changes'),
    path('newPatient/record/record',views.record,name = 'record'),
]
