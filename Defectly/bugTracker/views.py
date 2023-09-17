from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Project, Bugs, Comments
from .forms import BugCreationForm, CommentCreationForm, ProjectCreationForm


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
    bugs_count = Bugs.objects.filter(assignees=request.user, open=True).count()
    resolved_count = Bugs.objects.filter(
        open=False, resolved_by=request.user).count()
    context = {
        "projects_count": projects_count,
        "bugs_count": bugs_count,
        "resolved_count": resolved_count
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

        # create a new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # add user to the developers group
        dev_group = Group.objects.get(name='Developer')
        user.groups.add(dev_group)

        login(request, user)
        return redirect('login')

    return render(request, 'register.html')


@login_required(login_url='login')
def project_view(request):
    project_form = ProjectCreationForm()
    projects = Project.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        form.save()

        context = {"projects": projects, "message": "Created successfully"}
        return render(request, "projects.html", context)

    context = {"projects": projects, "project_form": project_form}
    return render(request, 'projects.html', context)


@login_required(login_url='login')
def bugs_view(request):
    bugs = Bugs.objects.filter(assignees=request.user, open=True)
    return render(request, 'bugs.html', {"bugs": bugs})


@login_required(login_url='login')
def project_info_view(request, id):
    project = Project.objects.get(pk=id)
    bugForm = BugCreationForm()
    bugs = project.bugs.filter(open=True)
    assigned_members = project.user

    context = {
        "project": project,
        "bugs": bugs,
        "bugForm": bugForm,
        "assigned_members": assigned_members
    }

    if request.method == 'POST':
        form = BugCreationForm(request.POST)
        if form.is_valid():
            bug_instance = form.save(commit=False)
            bug_instance.project = project
            bug_instance.created_by = request.user
            bug_instance.save()

            team_members = request.POST.getlist('team_members')
            bug_instance.assignees.set(team_members)
            return render(request, "project_info.html", context)

    return render(request, "project_info.html", context)


@login_required(login_url='login')
def bug_info(request, id):
    commentForm = CommentCreationForm()
    bug = Bugs.objects.get(pk=id)
    comments = bug.comments.all()
    context = {
        "commentForm": commentForm,
        "bug": bug,
        "comments": comments
    }

    if request.method == 'POST':
        # check if user wants to close a bug report
        if request.POST.get('bug_status_change'):
            bug_id_to_change = request.POST.get('bug_status_change')
            bug_to_change = Bugs.objects.get(pk=bug_id_to_change)
            bug_to_change.open = False
            bug_to_change.resolved_by = request.user
            bug_to_change.save()

        # check if the user wants to delete comment
        elif request.POST.get('delete_post'):
            comment_id_to_delete = request.POST.get('delete_post')
            comment_to_delete = Comments.objects.get(pk=comment_id_to_delete)
            comment_to_delete.delete()

        # create new comment
        else:
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.instance.author = request.user
                form.instance.bug = bug
                form.save()

        return redirect('bugInfo', bug.id)

    return render(request, 'bug_info.html', context)


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

        # check if user is an admin
        admin_group = Group.objects.get(name='Admins')
        is_admin = admin_group in user.groups.all()

        return render(request, 'administration.html', {
            "bugs": bugs,
            "selected_user": user,
            "projects": projects,
            "users": users,
            "is_admin": is_admin,
            "resolves": resolves
        })

    return render(request, 'administration.html', {
        "users": users
    })


def logout_view(request):
    logout(request)
    return redirect('login')
