from pydoc import doc
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import speech_recognition as sr
import pyaudio
import re
import string
from datetime import date
import numpy as np
import spacy
import scispacy
from torch import DoubleStorage

from app.models import Doctor

nlp = spacy.load("en_ner_bc5cdr_md")

# sample = "The patient has symtoms of fever, vommiting & weakness hence he is diagnosed with diarrohea. He can take an over-the-counter medicine such as bismuth subsalicylate or loperamide, which you can get as liquids or tablets."
# sample = "The patient has Type 2 diabetes. Take Metformin Fortamet Glumetza 120 mg twice a day for 6 months."
# sample= "Take 500 mg atropine twice a day for 5 days for cancer."

from fpdf import FPDF
import os, sys

# Create your views here.
global audio_text
global text_area
global data
global disease
audio_text = ""
text_area = ""
global count
count = False
rows, cols = (20, 4)
data = [["" for i in range(cols)] for j in range(rows)]


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
        hospital = request.POST['hospital']

        user = User.objects.create_user(
            password=password,
            email=email,
            first_name=name,
            username=username
        )

        user.save()

        doctor = Doctor(d_email=email, d_name=name, d_contactNo=contact_no, state=state, city=city, hospital_name=hospital, specialization=speciality)
        doctor.save()

        # speciality_record = Specialization(doctor_id=doctor.doctor_id, description=speciality)
        # speciality_record.save()

        print('User created: ', doctor.doctor_id)
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
    test_input = globals()['audio_text']
    extract_ner(test_input)
    return render(request, 'signature.html')
    # return render(request, 'record-proceed.html', {'audio_text': globals()['audio_text']})

def extract_ner(text):
    doc = nlp(text)
    #chemical and disease
    print("TEXT","ENTITY TYPE")
    i = 0
    for ent in doc.ents:
        print(ent.text+" : " + ent.label_)
        if ent.label == 'CHEMICAL':
            globals()['data'][i][0] = ent.text
            i = i + 1
        elif ent.label == 'DISEASE':
            globals()['disease'] = ent.text
    # dosage
    dosage = re.findall("[0-9]+mg|[0-9]+ml|[0-9]+\smg|[0-9]+\sml", text)
    #duration/frequency
    freq = re.findall("[0-9]+\smonth|[0-9]+\sday|[0-9]+\sweek|[0-9]+\smonths|[0-9]+\sdays|[0-9]+\sweeks|[0-9]*\sdaily|[0-9]*\stimes\sdaily|monthly|night|evening|morning|afternoon|twice|once|thrice ", text)
    #form
    
    i = 0
    for x in dosage:
        print(x," : DOSAGE")
        globals()['data'][i][1] = x
        i = i + 1
    i = 0
    for x in freq:
        print(x," : FREQUENCY")
        globals()['data'][i][2] = x
        i = i + 1

    print(globals()['data'])

def generate(request):
    if request.method == 'GET':

        current_user = request.user
        email_id = current_user.email
        
        doctor = Doctor.objects.get(d_email=email_id)
        doctor_name = doctor.d_name
        doctor_contact = doctor.d_contactNo
        hospital_name = doctor.hospital_name
        specialization = doctor.specialization

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.set_fill_color(102,224,255)
        pdf.cell(190, 20,'PRESCRIBOMETER', 0, 1, 'C', fill=True)
        # pdf.cell(200, 10, txt = "",ln = 1, align = 'C')

        current_date = date.today()
        pdf.set_font("Arial", size = 15)
        pdf.cell(190, 10, txt = hospital_name.upper() ,ln = 1, align = 'C')
        pdf.set_font("Arial", size = 12)
        pdf.cell(190, 10, txt = "Dr. " + doctor_name ,ln = 1, align = 'L')
        pdf.cell(190, 10, txt = specialization, ln = 1, align = 'L')
        # pdf.cell(190, 10, txt = "Date: ", ln = 1, align = 'L')
        pdf.cell(190, 10, txt = "Email: " + email_id ,ln = 1, align = 'L')
        pdf.cell(190, 10, txt = "Contact: " + str(doctor_contact) ,ln = 1, align = 'L')
        pdf.cell(190, 10, txt = "",ln = 1, align = 'C')
        pdf.cell(190, 10, txt = "Diagnosed with :",ln = 1, align = 'L')
        pdf.cell(190, 10, txt = "",ln = 1, align = 'C')

        # Table
        data = [
                ['DRUG', 'DOSAGE', 'DURATION', 'FORM'],
                ['Crocin', '120mg', '2 months', 'oral'],
                ]
        # data = globals()['data']
        spacing = 2
        pdf.set_font("Times", size=12)
        #pdf.add_page()
   
        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height*spacing,txt=item, border=1)
            pdf.ln(row_height*spacing)
        
        pdf.set_y(-10)
        pdf.set_font('Arial', 'I', 8)
        page = 'Page ' + str(pdf.page_no())
        
        pdf.cell(0, 10, page, 0, 0, 'C')
        pdf.add_page()
        pdf.image('C:/Users/hp/Downloads/signature.png', x=2, y=2)

        # save the pdf with name .pdf
        pdf.output("prescription.pdf")
        os.startfile('prescription.pdf', 'open')
    return render(request, 'dashboard.html')
