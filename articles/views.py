from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from articles.models import Article, Keyword, Ranking
from articles.forms import UpdateArticleForm, KeywordForm

from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq
from articles.management.commands.utils.generate_keywords_api import generate_keywords_api

from projects.models import Project
from projects.views import project_list

from accounts.models import User

from urllib.parse import urlparse
from datetime import date


@login_required
def article_detail(request, article_id):
    current = Article.objects.get(id=article_id)
    if request.method == 'POST':
        aform = UpdateArticleForm(request.POST)
        kform = KeywordForm(request.POST)
        if aform.is_valid():
            p = Project.objects.get(id=request.POST.get('project_id'))
            u = User.objects.get(id=request.POST.get('person_in_charge'))
            current.project_id = p
            current.url = request.POST.get('url')
            current.title = request.POST.get('title')
            current.published_at = request.POST.get('published_at')
            current.updated_at = request.POST.get('updated_at')
            current.person_in_charge = u
            current.save()
            messages.add_message(request, messages.SUCCESS,
                                "記事詳細設定を更新しました。")
            return redirect(article_detail, article_id=article_id)
        elif kform.is_valid(): 
            keywords = request.POST.get('keyword')
            lst = keywords.split('\n')
            keyword = []
            for e in lst:
                elst = e.split()
                keyword.append(" ".join(elst))
            keyword = list(set(keyword))
            for e in keyword:
                klst = Keyword.objects.filter(keyword=e)
                if len(klst) == 0:
                    k = Keyword.objects.create(
                        keyword=e,
                        volume=generate_keywords_api(e),
                        updated_at=date.today()
                    )
                    current.keywords.add(k)
                else:
                    alst = Article.objects.filter(keywords__keyword=e)
                    if not current in alst:
                        current.keywords.add(klst[0])
            messages.add_message(request, messages.ERROR,
                                 "キーワードを登録しました。")
        else:
            messages.add_message(request, messages.ERROR,
                                 "キーワードの登録に失敗しました。")
    projects = request.user.members_projects.all()
    members = current.project_id.members.all()
    context = {
        'current': current,
        'projects': projects,
        'members': members,
        'keywords': current.keywords.all()
    }
    return render(request, 'articles/detail.html', context)
    
@login_required
def delete_keywords(request, article_id):
    current = Article.objects.get(id=article_id)
    if request.POST.get('keyword'):
        for k in request.POST.getlist('keyword'):
            keyword = Keyword.objects.filter(keyword=k)
            current.keywords.remove(keyword[0])
    return redirect(article_detail, article_id=article_id)