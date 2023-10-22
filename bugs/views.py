from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import CommentCreationForm
from core.models import Comments
from .models import Bugs


@login_required(login_url='login')
def bugs_view(request):
    bugs = Bugs.objects.filter(assignees=request.user, open=True)
    return render(request, 'bug/bugs.html', {"bugs": bugs, "section": "bugs"})


@login_required(login_url='login')
def bug_info(request, id):
    commentForm = CommentCreationForm()
    bug = Bugs.objects.get(pk=id)
    comments = bug.comments.all()
    context = {
        "commentForm": commentForm,
        "bug": bug,
        "comments": comments,
        "section": "bugs"
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

    return render(request, 'bug/bug_info.html', context)
