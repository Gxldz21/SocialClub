from django import forms
from .models import *


class CreationPost(forms.ModelForm):
    group = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ('text', 'image')

    # def clean(self):
    #     likes = self.cleaned_data.get('group')
    #     if likes is None:
    #         self.cleaned_data['group'] = None
    #     return self.cleaned_data
