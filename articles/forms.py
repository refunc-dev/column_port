from django import forms

from articles.models import Article


class UpdateArticleForm(forms.ModelForm):
    category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Article
        fields = ('project', 'path', 'title', 'published_at', 'updated_at', 'person_in_charge', 'category')


class AddArticleForm(forms.ModelForm):
    category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Article
        fields = ('path', 'title', 'published_at', 'updated_at', 'person_in_charge', 'category')