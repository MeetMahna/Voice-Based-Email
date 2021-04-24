from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from .models import User
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("myapp:home")
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            # login(request, user)
            return redirect("myapp:login")
        else:
            return render(request, 'myapp/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'myapp/signup.html', {'form': form})


def home_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("myapp:first")

    context['auth_code'] = user.auth_code
    context['email'] = user.email
    return render(request, 'myapp/home.html', context)


def first(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("myapp:home")

    return render(request, 'myapp/first.html', context)


def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return


def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        # texttospeech("speak", file + i)
        # i = i + str(1)
        # playsound('output.mp3')
        print("Speak Now")
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
        print(response)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp.strip()

# def login_view(request):
#     context = {}
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method == 'POST':
#         print(request.POST)
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             auth_code = form.cleaned_data.get('auth_code')
#             user = authenticate(email=email, password=password)
#             # print("valid")
#             if user is not None and auth_code == user.auth_code:
#                 login(request, user)
#                 return redirect("myapp:home")
#             else:
#                 context['form'] = form
#
#         else:
#             try:
#                 acc = User.objects.get(email=request.POST['email'])
#
#             except User.DoesNotExist:
#                 context['message'] = 'Please enter correct email and password !'
#             context['form'] = form
#     else:
#         context['form'] = LoginForm()
#     return render(request, 'myapp/login.html', context)


def logout_view(request):
    logout(request)
    return redirect("myapp:first")


def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("myapp:home")
    

    

    
    
    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Email Portal. Login with your email account to continue. "
        file = 'test'
        i = '1'
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            if addr != 'N':
                texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
                
                i = i + str(1)
                say = speechtotext(10)
                print(say)
                if say == 'yes' or say == 'Yes' or say=='yes yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
            addr = addr.strip()
            addr = addr.replace(' ', '')
            addr = addr.lower()
            addr = convert_special_char(addr)
        flag = True
        while (flag):
            texttospeech("Enter your Password", file + i)
            i = i + str(1)
            passs = speechtotext(10)
            if addr != 'N':
                texttospeech("You meant " + passs + " say yes to confirm or no to enter again", file + i)
                
                i = i + str(1)
                say = speechtotext(10)
                print(say)
                if say == 'yes' or say == 'Yes' or say=='yes yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
            passs = passs.strip()
            passs = passs.replace(' ', '')
            passs = passs.lower()
            passs = convert_special_char(passs)


        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            auth_code = form.cleaned_data.get('auth_code')
            user = authenticate(email=em, password=pas)
            print("************USER******=", user)
            print("valid")
            if user is not None and auth_code == user.auth_code:
                login(request, user)
                return redirect("myapp:home")
            else:
                context['form'] = form
                context['message'] = 'Incorrect Authentication Code!'
        else:
            print(addr)
            print('tf')
            context['message'] = 'Please enter correct email and password !'
            context['form'] = form
    else:
        context['form'] = LoginForm()
        

    return render(request, 'myapp/login.html', context)

