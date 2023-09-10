from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project


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


@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        
        # check for duplicate email
        if User.objects.filter(email=email).exists():
            context = {"message": "Account with email already exists"}
            return render(request, 'register.html', context)
        
        if password != confirm:
            context = {"message": "Passwords must match"}
            return render(request, "register.html", context)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


@login_required(login_url='login')
def project_view(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        description = request.POST['description']
        current_user = request.user
        new_project = Project(
            name=project_name,
            description=description,
        )
        # save new project
        new_project.save()
        new_project.user.add(current_user)

        # retrieve all projects
        projects = request.user.projects.all()
        context = {"projects": projects, "message": "Created successfully"}
        return render(request, "projects.html", context)

    projects = request.user.projects.all()
    context = {"projects": projects}
    return render(request, 'projects.html', context)


@login_required(login_url='login')
def project_info_view(request, id):
    project = Project.objects.get(pk=id)
    context = {"project": project}
    return render(request, "project_info.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')
