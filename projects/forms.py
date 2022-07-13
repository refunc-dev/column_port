from django import forms

from projects.models import Website, Keyword, Project
from colorfield.widgets import ColorWidget


class ProjectRegisterForm(forms.Form):
    name = forms.CharField(max_length=128)
    domain = forms.CharField(max_length=2083)


class ProjectCompetitorForm(forms.Form):
    domain = forms.CharField(max_length=2083) 
    color = forms.CharField(widget=ColorWidget)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('keyword',)