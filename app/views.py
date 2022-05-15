from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
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
    return render(request, 'register.html')


def profile(request):
    return render(request, 'profile.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def newPatient(request):
    return render(request, 'new-patient.html')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'dashboard.html')
        else:
            return redirect('/')
    else:
        return render(request, 'index.html')


def userRegistration(request):
    if request.method == 'POST':
        name = request.POST['name']
        # username = request.POST['username']
        email = request.POST['email']
        contact_no = request.POST['contact_no']
        password = request.POST['password']
        state = request.POST['state']
        city = request.POST['city']
        speciality = request.POST['speciality']
        username = email

        user = User.objects.create_user(
            password=password,
            email=email,
            first_name=name,
            username=username
        )

        user.save()
        print('User created')
        return redirect('/')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def record(request):
    if request.method == 'GET':
        data = request.GET['fulltextarea']
        globals()['text_area'] = data
    globals()['audio_text'] = globals()['audio_text']
    # Removed
    globals()['count'] = not globals()['count']
    while globals()['count'] == True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.1)
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
    return render(request, 'new-patient.html', {'audio_text': globals()['audio_text']})


def save_changes(request):
    globals()['count'] = not globals()['count']
    if(globals()['text_area'] != ""):
        data = globals()['text_area']
        globals()['audio_text'] = data
        print(globals()['audio_text'])
    return render(request, 'new-patient.html', {'audio_text': globals()['audio_text']})
