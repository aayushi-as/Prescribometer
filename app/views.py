from django.shortcuts import render
import speech_recognition as sr
import pyaudio

# Create your views here.
global audio_text
global text_area
audio_text = ""
text_area = ""
global count
count = False
def get_audio_text():
    return globals()['audio_text']

def set_audio_text(text):
    globals()['audio_text'] = text

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
    if request.method == 'GET':
        data = request.GET['fulltextarea']
        globals()['text_area'] = data  
    globals()['audio_text'] = globals()['audio_text']
    #Removed
    globals()['count'] = not globals()['count']
    while globals()['count'] == True:
         r = sr.Recognizer()
         with sr.Microphone() as source:
             r.adjust_for_ambient_noise(source,duration=0.1)
             audio_data = r.listen(source)
             print("Recognizing...")
             try:
                 audio_text = r.recognize_google(audio_data)
                 globals()['audio_text'] = globals()['audio_text'] + audio_text
                 print("Text: "+globals()['audio_text'])
             except:
                 audio_text = ""
                 globals()['audio_text'] = globals()['audio_text'] + audio_text
                 print("Sorry, I did not get that")
    return render(request,'new-patient.html',{'audio_text':globals()['audio_text']})
def save_changes(request):
    globals()['count'] = not globals()['count']
    if(globals()['text_area'] != ""):
        data = globals()['text_area']
        globals()['audio_text'] = data
        print(globals()['audio_text'])
    return render(request, 'new-patient.html',{'audio_text':globals()['audio_text']})
    
