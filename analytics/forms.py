from django import forms

from analytics.models import Regex


class RegexForm(forms.ModelForm):
    class Meta:
        model = Regex
        fields = ('regex', 'name')