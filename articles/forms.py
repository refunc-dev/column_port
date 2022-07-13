from django import forms

from articles.models import Article


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('project', 'path', 'title', 'published_at', 'updated_at', 'person_in_charge', 'category')


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('path', 'title', 'published_at', 'updated_at', 'person_in_charge', 'category')