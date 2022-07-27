from django import forms

from projects.models import Website, Keyword, Project
from colorfield.widgets import ColorWidget


class ProjectRegisterForm(forms.Form):
    name = forms.CharField(max_length=128)
    domain = forms.CharField(max_length=2083)
    account_id = forms.CharField(max_length=20, required=False)
    property_id = forms.CharField(max_length=30, required=False)
    view_id = forms.CharField(max_length=30, required=False)


class ProjectCompetitorsForm(forms.Form):
    domain = forms.CharField(max_length=2083) 
    name = forms.CharField(max_length=100)


class ProjectAnalyticsForm(forms.Form):
    account_id = forms.CharField(max_length=20) 
    property_id = forms.CharField(max_length=30)
    view_id = forms.CharField(max_length=30)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('keyword',)