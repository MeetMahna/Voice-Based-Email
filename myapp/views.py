from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from .models import User


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
            return redirect('login/')
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
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            auth_code = form.cleaned_data.get('auth_code')
            user = authenticate(email=email, password=password)
            print("************USER******=", user)
            print("valid")
            if user is not None and auth_code == user.auth_code:
                login(request, user)
                return redirect("myapp:home")
            else:
                context['form'] = form
                context['message'] = 'Incorrect Authentication Code!'
        else:
            context['message'] = 'Please enter correct email and password !'
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'myapp/login.html', context)

