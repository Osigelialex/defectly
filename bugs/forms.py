from django import forms
from .models import Bugs


class BugCreationForm(forms.ModelForm):
    SEVERITY_CHOICES = [
        ('high', 'High'),
        ('mid', 'Mid'),
        ('low', 'Low')
    ]

    severity = forms.ChoiceField(
        choices=SEVERITY_CHOICES,
        initial='mid',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ))

    class Meta:
        model = Bugs
        fields = ['title', 'description', 'severity']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title of bug',
                'id': 'floatingTextarea',
                'class': 'form-control',
                'required': True
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description of bug',
                'id': 'floatingTextarea',
                'class': 'form-control mb-4',
                'style': 'height: 100px;',
                'required': True
            })
        }