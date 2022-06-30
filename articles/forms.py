from django import forms

from articles.models import Article, Keyword

class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('project_id', 'url', 'title', 'published_at', 'updated_at', 'person_in_charge')

class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('url', 'title', 'published_at', 'updated_at', 'person_in_charge')

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('keyword',)