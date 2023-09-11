from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Bugs, Comments
from .forms import BugCreationForm, CommentCreationForm


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
    bugForm = BugCreationForm()
    bugs = project.bugs.all()
    context = {"project": project, "bugs": bugs, "bugForm": bugForm}

    if request.method == 'POST':
        form = BugCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.project = project
            form.instance.created_by = request.user
            form.save()
            return render(request, "project_info.html", context)

    return render(request, "project_info.html", context)


@login_required(login_url='login')
def comments_view(request):
    pass
        


@login_required(login_url='login')
def bug_info(request, id):
    commentForm = CommentCreationForm()
    bug = Bugs.objects.get(pk=id)
    comments = Comments.objects.all()
    context = {"commentForm": commentForm, "bug": bug, "comments": comments}

    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            form.instance.bug = bug
            form.save()
            return render(request, 'bug_info.html', context)
    
    return render(request, 'bug_info.html', context)
        

def logout_view(request):
    logout(request)
    return redirect('login')
