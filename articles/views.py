from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from articles.models import Article, Keyword, Ranking
from articles.forms import ArticleForm, KeywordForm

from projects.views import project_list


@login_required
def keyword_new(request, article_id):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.save(commit=False)
            keyword.save()
            messages.add_message(request, messages.SUCCESS,
                                "スニペットを作成しました。")
            return redirect(project_list)
        else:
            messages.add_message(request, messages.ERROR,
                                 "スニペットの作成に失敗しました。")
    else:
        form = KeywordForm()
    return render(request, 'articles/keyword_new.html', {'form': form})


def article_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            messages.add_message(request, messages.SUCCESS,
                                "スニペットを作成しました。")
            return redirect(article_list)
        else:
            messages.add_message(request, messages.ERROR,
                                 "スニペットの作成に失敗しました。")
    else:
        form = ArticleForm()
    return render(request, 'articles/new.html', {'form': form})


@login_required
def article_detail(request, article_id):
    articles = Article.objects.filter(article_id=article_id).all()
    context = {"articles": articles}
    return render(request, 'articles/detail.html', context)