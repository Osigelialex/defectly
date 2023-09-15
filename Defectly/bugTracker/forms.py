from django import forms
from .models import Bugs, Comments, Project


class BugCreationForm(forms.ModelForm):
    SEVERITY_CHOICES = [
        ('high', 'High'),
        ('mid', 'Mid'),
        ('low', 'Low')
    ]

    severity = forms.ChoiceField(choices=SEVERITY_CHOICES, initial='mid', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Bugs
        fields = ['title', 'description', 'severity', 'assignees']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title of bug', 'id': 'floatingTextarea', 'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description of bug', 'id': 'floatingTextarea', 'class': 'form-control mb-4', 'style': 'height: 100px;', 'required': True})
        }


class CloseBugForm(forms.ModelForm):
    class Meta:
        model = Bugs
        fields = ['bug_fix']

        widgets = {
            'bug_fix': forms.Textarea(attrs={'placeholder': 'Enter bug fix', 'id': 'floatingTextarea', 'class': 'form-control mb-4', 'style': 'height: 100px', 'required': True})
        }


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'user']
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter project name', 'id': 'floatingTextarea', 'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description of project', 'id': 'floatingTextarea', 'class': 'form-control mb-4', 'style': 'height: 100px;', 'required': True}),
        }


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add comment', 'id': 'floatingTextarea', 'class': 'form-control', 'style': 'height: 50px;', 'required': True})
        }