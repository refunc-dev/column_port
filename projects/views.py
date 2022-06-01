from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project, Regex, WeeklyAll, MonthlyAll, WeeklyDir, MonthlyDir
from projects.forms import ProjectForm, RegexForm
from articles.models import Article, Keyword, Ranking, Analytics
from articles.forms import ArticleForm

from projects.management.commands.utils.get_all_analytics_data import get_weekly_analytics_data, get_monthly_analytics_data
from projects.management.commands.utils.get_specific_analytics_data import get_weekly_analytics_data_regex, get_monthly_analytics_data_regex
from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq
from urllib.parse import urlparse


@login_required
def top(request):
    return redirect(project_list)


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


@login_required
def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
                name=request.POST.get('name'),
                url=request.POST.get('url'),
                created_by=request.user
            )
            data = get_weekly_analytics_data(24)
            for d in data:
                WeeklyAll.objects.create(
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    direct=d['direct'],
                    organic=d['organic'],
                    paid=d['paid'],
                    referral=d['referral'],
                    display=d['display'],
                    social=d['social'],
                    email=d['email'],
                    others=d['others'],
                    project_id=project
                )   
            data = get_monthly_analytics_data(24)
            for d in data:
                MonthlyAll.objects.create(
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    direct=d['direct'],
                    organic=d['organic'],
                    paid=d['paid'],
                    referral=d['referral'],
                    display=d['display'],
                    social=d['social'],
                    email=d['email'],
                    others=d['others'],
                    project_id=project
                )
            return redirect(project_list)
    else:
        form = ProjectForm()
    return render(request, 'projects/new.html', {'form': form})


@login_required
def project_detail(request, project_id):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            path = urlparse(article.url).path
            res = get_analytics_data_eq(path, 6)
            for data in reversed(res):
                Analytics.objects.create(
                    path=data['path'],
                    year_week=data['year_week'],
                    session=data['session'],
                    conversion_rate=data['cvr'],
                    conversion=data['cv'],
                    article_id=article
                )
            return redirect(project_detail, project_id=project_id)
    else:
        contents = []
        articles = Article.objects.filter(project_id=project_id).all()
        for article in articles:
            analytic = Analytics.objects.filter(article_id=article.id).order_by().reverse()[:6]
            session = {"1": "-","2": "-","3": "-","4": "-","5": "-","6": "-"}
            cvr = {"1": "-","2": "-","3": "-","4": "-","5": "-","6": "-"}
            cv = {"1": "-","2": "-","3": "-","4": "-","5": "-","6": "-"}
            for i, a in enumerate(analytic):
                session[f"{i + 1}"] = a.session
                cvr[f"{i + 1}"] = a.conversion_rate
                cv[f"{i + 1}"] = a.conversion
            klist = []
            keywords = Keyword.objects.filter(article_id=article.id).all()
            size = len(keywords)
            if size == 0:
                size = 1
            else:
                for k in keywords:
                    ranking = Ranking.objects.filter(keyword_id=k.id).order_by('date').reverse()[:6]
                    kdata = {
                        "keyword": k.keyword,
                        "volume": k.volume,
                        "1": "-",
                        "2": "-",
                        "3": "-",
                        "4": "-",
                        "5": "-",
                        "6": "-",
                        "right_wrong": "-",
                        "ranking_page": "-"
                    }
                    for i, r in enumerate(ranking):
                        if i == 0:
                            kdata["ranking_page"] = r.ranking_page
                            kdata["right_wrong"] = r.get_right_wrong_display()
                        kdata[f"{i + 1}"] = r.ranking
                    klist.append(kdata)
            contents.append({'article': article, 'keywords': klist, 'session': session, 'cvr': cvr, 'cv': cv, 'size': size})
        form = ArticleForm()
        context = {
            'id': project_id,
            'articles': contents,
            'form': form
        }
    return render(request, 'projects/detail.html', context)

@login_required
def report_weekly(request, project_id):
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = form.save(commit=False)
            regex.project_id = project_id
            regex.save()
            return redirect(report_weekly, project_id=project_id)
    else:
        regex = Regex.objects.filter(project_id=project_id)
        weekly = WeeklyAll.objects.filter(project_id=project_id).order_by('date').reverse()[:24]
        form = RegexForm()
        data = []
        for w in reversed(weekly):
            data.append([str(w.date), w.session, w.conversion_rate])
        context = {
            'term': {'ja': '年週', 'en': 'YearWeek'},
            'id': project_id,
            'data': data,
            'form': form
        }
    return render(request, 'projects/report.html', context)

@login_required
def report_monthly(request, project_id):
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = form.save(commit=False)
            regex.project_id = project_id
            regex.save()
            return redirect(report_monthly, project_id=project_id)
    else:
        regex = Regex.objects.filter(project_id=project_id)
        monthly = MonthlyAll.objects.filter(project_id=project_id).order_by('date').reverse()[:24]
        form = RegexForm()
        data = []
        for m in reversed(monthly):
            data.append([str(m.date), m.session, m.conversion_rate])
        context = {
            'term': {'ja': '年月', 'en': 'YearMonth'},
            'id': project_id,
            'data': data,
            'form': form
        }
    return render(request, 'projects/report.html', context)