from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from project.models import Project
from bugs.models import Bugs


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
            return render(request, "auth/login.html", context)
    return render(request, "auth/login.html")


@login_required(login_url='login')
def dashboard(request):
    projects_count = Project.objects.filter(user=request.user).count()
    bugs_count = Bugs.objects.filter(assignees=request.user, open=True).count()
    resolved_count = Bugs.objects.filter(
        open=False, resolved_by=request.user).count()
    context = {
        "projects_count": projects_count,
        "bugs_count": bugs_count,
        "resolved_count": resolved_count,
        "section": "dashboard"
    }

    return render(request, "dashboard/dashboard.html", context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        # check for duplicate email
        if User.objects.filter(email=email).exists():
            context = {"message": "Account with email already exists"}
            return render(request, 'auth/register.html', context)

        if password != confirm:
            context = {"message": "Passwords must match"}
            return render(request, "auth/register.html", context)

        # create a new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('login')

    return render(request, 'auth/register.html')


@login_required(login_url='login')
def administration(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)

        # retrieve user details
        bugs = Bugs.objects.filter(assignees=user, open=True).count()
        projects = Project.objects.filter(user=user).count()
        resolves = Bugs.objects.filter(resolved_by=user).count()
        
        is_admin = user.is_staff

        return render(request, 'admin/administration.html', {
            "bugs": bugs,
            "selected_user": user,
            "projects": projects,
            "users": users,
            "is_admin": is_admin,
            "resolves": resolves,
            "section": "administration"
        })

    return render(request, 'admin/administration.html', {
        "users": users,
        "section": "administration"
    })


def logout_view(request):
    logout(request)
    return redirect('login')
