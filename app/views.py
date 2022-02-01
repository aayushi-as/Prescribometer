from django.shortcuts import render

# Create your views here.
def index(request): 
    return render(request, 'index.html')

def register(request):
    return render(request,'register.html')

def profile(request): 
    return render(request, 'profile.html')

def analytics(request): 
    return render(request, 'analytics.html')

def dashboard(request): 
    return render(request, 'dashboard.html')

def newPatient(request): 
    return render(request, 'new-patient.html')

def existingPatient(request): 
    return render(request, 'existing-patients.html')