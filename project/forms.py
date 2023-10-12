from django import forms
from .models import Project


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'user']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter project name',
                'id': 'floatingTextarea',
                'class': 'form-control',
                'required': True
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description of project',
                'id': 'floatingTextarea',
                'class': 'form-control mb-4',
                'style': 'height: 100px;',
                'required': True
            }),

            'user': forms.SelectMultiple(attrs={
                'class': 'form-control'
            })
        }