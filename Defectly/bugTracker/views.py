from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def index(request):
    return HttpResponse("Hello")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def register(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')