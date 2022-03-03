from django.shortcuts import render
import speech_recognition as sr


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

def record(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio_data = r.listen(source)
        print("Recognizing...")
        try:
            # using google speech recognition
            print("Text: "+r.recognize_google(audio_data))
        except:
            print("Sorry, I did not get that")
    return render(request, 'existing-patients.html')