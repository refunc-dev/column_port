from django import forms

from projects.models import Project, Regex

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class RegexForm(forms.ModelForm):
    class Meta:
        model = Regex
        fields = '__all__'