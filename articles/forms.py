from django import forms

from articles.models import Article, Keyword

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('keyword',)