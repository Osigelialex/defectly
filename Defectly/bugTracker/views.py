from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

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
            return redirect('dashboard')
        else:
            context = {"message": "Invalid username or password"}
            return render(request, "login.html", context)
    return render(request, "login.html")


def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        if password != confirm:
            context = {"message": "Passwords must match"}
            return render(request, "register.html", context)
        else:
            user = User(username=username, password=password, email=email)
            user.save()
            return redirect('dashboard')
    return render(request, 'register.html')


def project_view(request):
    projects = request.user.projects.all()
    context = { "projects": projects }
    return render(request, 'projects.html', context) 


def logout_view(request):
    logout(request)
    return redirect('login')