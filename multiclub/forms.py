from django import forms
from .models import *


class CreationPost(forms.ModelForm):
    group = forms.CharField(required=False)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'tags')
