from django import forms
from .models import Comments


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Add comment',
                'id': 'floatingTextarea',
                'class': 'form-control',
                'style': 'height: 50px;',
                'required': True
            })
        }
