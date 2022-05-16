from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import speech_recognition as sr
import pyaudio
import re
import string
import joblib
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model



#joblib imports
word2idx = joblib.load('./model/word2idx.sav')
words = joblib.load('./model/words.sav')
tags = joblib.load('./model/tags.sav')
#model = joblib.load('./model/model.sav')
model = keras.models.load_model('./model/model_weights.h5')



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


def proceed(request):
    return render(request, 'record-proceed.html', {'audio_text': globals()['audio_text']})
def save_changes(request):
    if request.method == 'GET':
         data = request.GET['fulltextarea']
         globals()['text_area'] = data
         globals()['audio_text'] = globals()['text_area']
    print(globals()['audio_text'])
    test_input = "Take Metformin Fortamet Glumetza twice a day for 6 months."
    extract_ner(test_input)
    return render(request, 'record-proceed.html', {'audio_text': globals()['audio_text']})

def extract_ner(text):
    re_tok = re.compile(f"([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])")
    sentence_test = re_tok.sub(r"  ", text).split()
    padded_sentence = sentence_test + [word2idx["ENDPAD"]] * (50 - len(sentence_test))
    padded_sentence = [word2idx.get(w, 0) for w in padded_sentence]
    pred = model.predict(np.array([padded_sentence]))
    pred = np.argmax(pred, axis=-1)
    print("{:15}\t {}\n".format("Word","Pred"))
    print("-" *30)
    for w, pre in zip(padded_sentence, pred[0]):
        if words[w-1] in text:
            print("{:15}\t{}".format(words[w-1], tags[pre]))
    #return null