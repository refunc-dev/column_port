from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ranking.models import Ranking
from projects.models import Keyword, Website, Project, WebsiteKeywordRelation, ProjectCompetitorRelation
from articles.models import Article

from projects.forms import KeywordForm

from projects.management.commands.utils.generate_keywords_api import generate_keywords_api

from urllib.parse import urlparse
import datetime
import math
import re


@login_required
def ranking_top(request, project_id):
    return redirect(ranking_all, project_id=project_id)


@login_required
def ranking_all(request, project_id):
    current = Project.objects.get(id=project_id)
    form = KeywordForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            article = request.POST.get('article')
            if article == '選択してください':
                article = None
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
                    if article:
                        Article.objects.get(id=article).keywords.add(k)
                    WebsiteKeywordRelation.objects.create(
                        website=current.website,
                        keyword=k,
                        project=current,
                        registered_by=request.user,
                    )
                    for c in current.competitors.all():
                        WebsiteKeywordRelation.objects.create(
                            website=c,
                            keyword=k,
                            registered_by=request.user,
                        ) 
                else:
                    if article:
                        a = Article.objects.get(id=article).keywords.add(k)
                        alst = Article.objects.filter(keywords__keyword=k)
                        if not a in alst:
                            a.keywords.add(k)
                    r = WebsiteKeywordRelation.objects.get_or_none(website=current.website,keyword=k)
                    if r:
                        r.project = current
                        r.save()
                    else:
                        WebsiteKeywordRelation.objects.create(
                            website=current.website,
                            keyword=k,
                            project=current,
                            registered_by=request.user,
                        )
                    exists = WebsiteKeywordRelation.objects.filter(keyword=k).values('website')
                    competitors = current.competitors.exclude(competitors_projects__website__in=exists)
                    for c in competitors:
                        WebsiteKeywordRelation.objects.create(
                            website=c,
                            keyword=k,
                            registered_by=request.user,
                        ) 
            messages.success(request, 'キーワードの登録に成功しました')
        else:
            messages.add_message(request, messages.ERROR,
                                 "キーワードの登録に失敗しました。")
        return redirect(ranking_all, project_id=project_id)
    keywords = WebsiteKeywordRelation.objects.filter(project=current)
    data = []
    for k in keywords:
        keyword = k.keyword
        ranking = Ranking.objects.filter(website=current.website,keyword=keyword).order_by('date').reverse()[:5]
        kdata = {
            "keyword": keyword.keyword,
            "volume": keyword.volume,
            "ranking": ['-','-','-','-','-'],
            "date": ['-','-','-','-','-'],
            "ranking_page": "-",
            "title_link": "-"
        }
        for i, r in enumerate(ranking):
            if i == 0:
                kdata["ranking_page"] = r.ranking_page
                kdata["title_link"] = r.title_link
            kdata["ranking"][4 - i] = r.ranking
            kdata["date"][4 - i] = r.date
        data.append(kdata)
    projects = request.user.members_projects.all()
    articles = Article.objects.filter(project=current)
    context = {
        'current': current,
        'projects': projects,
        'articles': articles,
        'keywords': data,
    }
    return render(request, 'ranking/ranking_all.html', context)


@login_required
def ranking_range(request, project_id):
    current = Project.objects.get(id=project_id)
    keywords = list(WebsiteKeywordRelation.objects.filter(project=current).values_list('keyword', flat=True))
    data = {
        'date': ['-','-','-','-','-','-','-','-','-','-'],
        'count': {
            'first': [0,0,0,0,0,0,0,0,0,0],
            'second': [0,0,0,0,0,0,0,0,0,0],
            'sixth': [0,0,0,0,0,0,0,0,0,0],
            'eleventh': [0,0,0,0,0,0,0,0,0,0],
            'thirtyfirst': [0,0,0,0,0,0,0,0,0,0],
            'fiftyfirst': [0,0,0,0,0,0,0,0,0,0],
            'outofrange': [0,0,0,0,0,0,0,0,0,0]
        },
        'data': {
            'first': [0,0,0,0,0,0,0,0,0,0],
            'second': [0,0,0,0,0,0,0,0,0,0],
            'sixth': [0,0,0,0,0,0,0,0,0,0],
            'eleventh': [0,0,0,0,0,0,0,0,0,0],
            'thirtyfirst': [0,0,0,0,0,0,0,0,0,0],
            'fiftyfirst': [0,0,0,0,0,0,0,0,0,0],
            'outofrange': [0,0,0,0,0,0,0,0,0,0]
        }
    }
    if len(keywords) > 0:
        date = list(Ranking.objects.filter(website=current.website,keyword__in=keywords).order_by('date').reverse().distinct()[:10].values_list('date', flat=True))
        for i, d in enumerate(date):
            data['date'][9 - i] = d.strftime('%-m / %-d')
            ranking = list(Ranking.objects.filter(website=current.website,keyword__in=keywords,date=d).values_list('ranking',flat=True))
            for r in ranking:
                if r == 1:
                    data['count']['first'][9 - i] += 1
                elif r > 1 and r <=5:
                    data['count']['second'][9 - i] += 1
                elif r > 5 and r <=10:
                    data['count']['sixth'][9 - i] += 1
                elif r > 10 and r <=30:
                    data['count']['eleventh'][9 - i] += 1
                elif r > 30 and r <=50:
                    data['count']['thirtyfirst'][9 - i] += 1
                elif r > 50 and r <=100:
                    data['count']['fiftyfirst'][9 - i] += 1
                elif r > 100:
                    data['count']['outofrange'][9 - i] += 1
            total = len(ranking)
            if total == 0:
                data['data']['first'][9-i] = 0
                data['data']['second'][9-i] = 0
                data['data']['sixth'][9-i] = 0
                data['data']['eleventh'][9-i] = 0
                data['data']['thirtyfirst'][9-i] = 0
                data['data']['fiftyfirst'][9-i] = 0
                data['data']['outofrange'][9-i] = 0
            else:
                data['data']['first'][9-i] = data['count']['first'][9-i] / total * 100
                data['data']['second'][9-i] = data['count']['second'][9-i] / total * 100
                data['data']['sixth'][9-i] = data['count']['sixth'][9-i] / total * 100
                data['data']['eleventh'][9-i] = data['count']['eleventh'][9-i] / total * 100
                data['data']['thirtyfirst'][9-i] = data['count']['thirtyfirst'][9-i] / total * 100
                data['data']['fiftyfirst'][9-i] = data['count']['fiftyfirst'][9-i] / total * 100
                data['data']['outofrange'][9-i] = data['count']['outofrange'][9-i] / total * 100
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'data': data,
    }
    return render(request, 'ranking/ranking_range.html', context) 


def define_step_size(max):
    chunk = math.ceil(math.ceil(max) / 5)
    digits = 10 ** (len(str(int(chunk))) - 1)
    return math.ceil(chunk / digits) * digits


def hex_to_rgba(value, opacity):
    h = value.lstrip('#')
    l = list(int(h[i:i+2], 16) for i in (0, 2, 4))
    l.append(opacity)
    return f'rgba{tuple(l)}'


def create_score(current):
    keywords = list(WebsiteKeywordRelation.objects.filter(project=current).values_list('keyword', flat=True))
    date = []
    score = {
        'date': ['-','-','-','-','-','-','-','-','-','-'],
        'score': [0,0,0,0,0,0,0,0,0,0],
        'rgba': hex_to_rgba(current.color, 0.8),
        'max': 0,
        'stepSize': 0
    }
    scoreMax = 0
    if len(keywords) > 0:
        date = list(Ranking.objects.filter(website=current.website,keyword__in=keywords).order_by('date').reverse().distinct()[:10].values_list('date', flat=True))
        score_tmp = [10,9,8,7,6,5,4,3,2,1]
        for i, d in enumerate(date):
            score['date'][9-i] = d.strftime('%-m / %-d')
            ranking = Ranking.objects.filter(website=current.website,keyword__in=keywords,date=d)
            for r in ranking:
                if r.ranking >= 1 and r.ranking <= 10:
                    score['score'][9-i] += score_tmp[r.ranking-1]
            scoreMax = max(score['score'][9-i], scoreMax)
    pc = ProjectCompetitorRelation.objects.filter(project=current)
    cdata = []
    for c in pc:
        citem = {'name': c.competitor.domain, 'score': [0,0,0,0,0,0,0,0,0,0], 'color': c.color, 'rgba': hex_to_rgba(c.color, 0.8)}
        for i, d in enumerate(date):
            ranking = Ranking.objects.filter(website=c.competitor,keyword__in=keywords,date=d)
            for r in ranking:
                if r.ranking >= 1 and r.ranking <= 10:
                    citem['score'][9-i] += score_tmp[r.ranking-1]
            scoreMax = max(citem['score'][9-i], scoreMax)
        cdata.append(citem)
    score['stepSize'] = define_step_size(scoreMax)
    score['max'] = score['stepSize'] * 5
    score['competitors'] = cdata
    return score


@login_required
def ranking_score(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        for k, v in request.POST.items():
            if k == 'project_color':
                current.color = v
                current.save()
            else:
                c = Website.objects.get_or_none(domain=k)
                if not c:
                    continue
                pc = ProjectCompetitorRelation.objects.get_or_none(project=current,competitor=c)
                pc.color = v
                pc.save()
        return redirect(ranking_score, project_id=project_id)
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'score': create_score(current),
    }
    return render(request, 'ranking/ranking_score.html', context) 