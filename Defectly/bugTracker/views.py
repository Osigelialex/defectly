from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Bugs, Comments
from .forms import BugCreationForm, CommentCreationForm, ProjectCreationForm, CloseBugForm


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
    projects_count = Project.objects.filter(user=request.user).count()
    bugs_count = Bugs.objects.filter(assignees=request.user).count()
    context = {
        "projects_count": projects_count,
        "bugs_count": bugs_count
    }

    return render(request, "dashboard.html", context)


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
    project_form = ProjectCreationForm()

    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        form.save()

        # retrieve all projects
        projects = request.user.projects.all()
        context = {"projects": projects, "message": "Created successfully"}
        return render(request, "projects.html", context)

    projects = Project.objects.filter(user=request.user)
    context = {"projects": projects, "project_form": project_form}
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
def bug_info(request, id):
    commentForm = CommentCreationForm()
    closeBugForm = CloseBugForm()
    bug = Bugs.objects.get(pk=id)
    comments = bug.comments.all()
    context = {
        "commentForm": commentForm, 
        "closeBugForm": closeBugForm, 
        "bug": bug, 
        "comments": comments
    }

    if request.method == 'POST':
        # check if the user wants to delete comment
        if request.POST.get('delete_post'):
            comment_id_to_delete = request.POST.get('delete_post')
            comment_to_delete = Comments.objects.get(pk=comment_id_to_delete)
            comment_to_delete.delete()
            return render(request, 'bug_info.html', context)

        # create new comment
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
