from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from articles.models import Article, ArticleAnalytics
from projects.models import Keyword, Website, Project, WebsiteKeywordRelation
from ranking.models import Ranking
from accounts.models import User

from articles.forms import UpdateArticleForm, AddArticleForm
from projects.forms import KeywordForm

from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq
from projects.management.commands.utils.generate_keywords_api import generate_keywords_api

from urllib.parse import urlparse
import datetime
import re


@login_required
def top(request, project_id):
    current = Project.objects.get(id=project_id)
    is_error = False
    if request.method == 'POST':
        form = AddArticleForm(request.POST)
        path = request.POST.get('path')
        if re.search(r'//', path):
            o = urlparse(path)
            host = o.hostname
            path = o.path
            if not host == current.website.domain:
                is_error = True
                messages.error(request, 'プロジェクトのドメインと一致しません')
            elif Article.objects.get_or_none(project=current,path=path):
                is_error = True
                messages.error(request, '既に登録済みの記事です')
        if form.is_valid() and not is_error:
            article = form.save(commit=False)
            article.path = path
            article.project = current
            article.person_in_charge = request.user
            article.created_by = request.user
            article.save()
            res = get_analytics_data_eq(path, 6)
            for data in reversed(res):
                ArticleAnalytics.objects.create(
                    article=article,
                    date=data['date'],
                    session=data['session'],
                    conversion=data['cv'],
                    conversion_rate=data['cvr'],
                )
            messages.success(request, '登録に成功しました')
        return redirect(top, project_id=project_id)
    contents = []
    articles = Article.objects.filter(project=current).all()
    for article in articles:
        analytic = ArticleAnalytics.objects.filter(article=article).order_by().reverse()[:5]
        date = {"1": "-","2": "-","3": "-","4": "-","5": "-"}
        session = {"1": "-","2": "-","3": "-","4": "-","5": "-"}
        cvr = {"1": "-","2": "-","3": "-","4": "-","5": "-"}
        cv = {"1": "-","2": "-","3": "-","4": "-","5": "-"}
        for i, a in enumerate(analytic):
            date[f"{i + 1}"] = a.date
            session[f"{i + 1}"] = a.session
            cvr[f"{i + 1}"] = a.conversion_rate
            cv[f"{i + 1}"] = a.conversion
        klist = []
        keywords = article.keywords.all()
        size = len(keywords)
        if size == 0:
            size = 1
        else:
            for k in keywords:
                ranking = Ranking.objects.filter(website=article.project.website,keyword_id=k).order_by('date').reverse()[:5]
                kdata = {
                    "keyword": k.keyword,
                    "volume": k.volume,
                    "ranking": ['-','-','-','-','-'],
                    "date": ['-','-','-','-','-'],
                    "right_wrong": "-",
                    "ranking_page": "-"
                }
                for i, r in enumerate(ranking):
                    if i == 0:
                        kdata["ranking_page"] = r.ranking_page
                        kdata["right_wrong"] = '○' if article.path == r.ranking_page else '×'
                    kdata["ranking"][4 - i] = r.ranking
                    kdata["date"][4 - i] = r.date
                klist.append(kdata)
        contents.append({'article': article, 'keywords': klist, 'session': session, 'cvr': cvr, 'cv': cv, 'size': size, 'date': date})
    members = current.members.all()
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'articles': contents,
        'members': members,
    }
    return render(request, 'articles/top.html', context)


@login_required
def settings(request, project_id, article_id):
    current = Article.objects.get(id=article_id)
    if request.method == 'POST':
        aform = UpdateArticleForm(request.POST)
        kform = KeywordForm(request.POST)
        if aform.is_valid():
            current.project = Project.objects.get(id=request.POST.get('project'))
            path = request.POST.get('path')
            if re.search(r'//', path):
                path = urlparse(domain).path
            current.path = path
            current.title = request.POST.get('title')
            current.published_at = request.POST.get('published_at')
            current.updated_at = request.POST.get('updated_at')
            current.person_in_charge = User.objects.get(id=request.POST.get('person_in_charge'))
            current.category = request.POST.get('category')
            current.save()
            messages.success(request, "設定を更新しました")
            return redirect(settings, project_id=project_id, article_id=article_id)
        elif kform.is_valid(): 
            keywords = request.POST.get('keyword')
            lst = keywords.split('\n')
            keyword = []
            for e in lst:
                elst = e.split()
                keyword.append(" ".join(elst))
            keyword = list(set(keyword))
            for e in keyword:
                k = Keyword.objects.get_or_none(keyword=e)
                if not k:
                    k = Keyword.objects.create(
                        keyword=e,
                        volume=generate_keywords_api(e),
                        registered_by=request.user,
                        updated_at=datetime.date.today() - datetime.timedelta(days=1),
                    )
                    current.keywords.add(k)
                    WebsiteKeywordRelation.objects.create(
                        website=current.project.website,
                        keyword=k,
                        project=current.project,
                        registered_by=request.user,
                    )
                    for c in current.project.competitors.all():
                        WebsiteKeywordRelation.objects.create(
                            website=c,
                            keyword=k,
                            registered_by=request.user,
                        ) 
                else:
                    alst = Article.objects.filter(keywords__keyword=k)
                    if not current in alst:
                        current.keywords.add(k)
                    r = WebsiteKeywordRelation.objects.get_or_none(website=current.project.website,keyword=k)
                    if r:
                        r.project = current.project
                        r.save()
                    else:
                        WebsiteKeywordRelation.objects.create(
                            website=current.project.website,
                            keyword=k,
                            project=current.project,
                            registered_by=request.user,
                        )
                    exists = WebsiteKeywordRelation.objects.filter(keyword=k).values('website')
                    competitors = current.project.competitors.exclude(competitors_projects__website__in=exists)
                    for c in competitors:
                        WebsiteKeywordRelation.objects.create(
                            website=c,
                            keyword=k,
                            registered_by=request.user,
                        ) 
            messages.success(request, 'キーワードの登録に成功しました')
        elif request.POST.get('delete'):
            current.delete()
            messages.success(request, '記事を削除しました')
            return redirect(top, project_id=project_id)
        else:
            messages.error(request, 'キーワードの登録に失敗しました')
        return redirect(settings, project_id=project_id, article_id=article_id)
    projects = request.user.members_projects.all()
    members = current.project.members.all()
    context = {
        'current': current,
        'projects': projects,
        'members': members,
        'keywords': current.keywords.all()
    }
    return render(request, 'articles/detail.html', context)


@login_required
def remove_keywords(request, project_id, article_id):
    current = Article.objects.get(id=article_id)
    if request.POST.get('keyword'):
        for k in request.POST.getlist('keyword'):
            keyword = Keyword.objects.get(id=k)
            current.keywords.remove(keyword)
    return redirect(settings, project_id=project_id, article_id=article_id)