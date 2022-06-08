from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from articles.models import Article, Keyword, Ranking
from articles.forms import ArticleForm, KeywordForm

from projects.views import project_list

from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq
from articles.management.commands.utils.generate_keywords_api import generate_keywords_api

from urllib.parse import urlparse
from datetime import date


@login_required
def keyword_new(request, article_id):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('keyword')
            k = Keyword.objects.create(
                keyword=keyword,
                volume=generate_keywords_api(keyword),
                updated_at=date.today()
            )
            article = Article.objects.get(id=article_id)
            article.keywords.add(k)
            messages.add_message(request, messages.SUCCESS,
                                "スニペットを作成しました。")
            return redirect(project_list)
        else:
            messages.add_message(request, messages.ERROR,
                                 "スニペットの作成に失敗しました。")
    else:
        form = KeywordForm()
    return render(request, 'articles/keyword_new.html', {'form': form})


@login_required
def article_detail(request, article_id):
    articles = Article.objects.filter(article_id=article_id).all()
    context = {"articles": articles}
    return render(request, 'articles/detail.html', context)