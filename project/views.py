from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project
from .forms import ProjectCreationForm
from bugs.forms import BugCreationForm


@login_required(login_url='login')
def project_view(request):
    project_form = ProjectCreationForm()
    projects = Project.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        form.save()

        context = {"projects": projects, "message": "Created successfully"}
        return render(request, "project/projects.html", context)

    context = {"projects": projects, "project_form": project_form, "section": "projects"}
    return render(request, 'project/projects.html', context)


@login_required(login_url='login')
def project_info_view(request, id):
    project = Project.objects.get(pk=id)
    bugForm = BugCreationForm()
    unassigned_devs = User.objects.exclude(projects=project)
    bugs = project.bugs.filter(open=True)
    assigned_members = project.user

    context = {
        "project": project,
        "bugs": bugs,
        "bugForm": bugForm,
        "unassigned_devs": unassigned_devs,
        "assigned_members": assigned_members,
        "section": "projects"
    }

    if request.method == 'POST':
        # check if user wants to add a new dev
        if request.POST.get('new_devs'):
            new_devs = request.POST.getlist('new_devs')
            project.user.add(*new_devs)
            return redirect(project_info_view, project.id)

        # create new bug ticket for user
        form = BugCreationForm(request.POST)
        if form.is_valid():
            bug_instance = form.save(commit=False)
            bug_instance.project = project
            bug_instance.created_by = request.user
            bug_instance.save()

            team_members = request.POST.getlist('team_members')
            bug_instance.assignees.set(team_members)
            return render(request, "project/project_info.html", context)

    return render(request, "project/project_info.html", context)