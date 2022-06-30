from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project, Regex, WeeklyAll, MonthlyAll, WeeklyDir, MonthlyDir
from projects.forms import ProjectForm, RegexForm
from articles.models import Article, Keyword, Ranking, Analytics
from articles.forms import UpdateArticleForm, AddArticleForm, KeywordForm
from accounts.models import User


from projects.management.commands.utils.get_all_analytics_data import get_weekly_analytics_data, get_monthly_analytics_data
from projects.management.commands.utils.get_specific_analytics_data import get_weekly_analytics_data_regex, get_monthly_analytics_data_regex
from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq
from articles.management.commands.utils.generate_keywords_api import generate_keywords_api

from urllib.parse import urlparse
from datetime import date
import math


@login_required
def project_list(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
                name=request.POST.get('name'),
                domain=request.POST.get('domain'),
                created_by=request.user
            )
            project.members.add(request.user)
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
                    organic_conversion=d['organic_conversion'],
                    organic_conversion_rate=d['organic_conversion_rate'],
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
                    organic_conversion=d['organic_conversion'],
                    organic_conversion_rate=d['organic_conversion_rate'],
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
        projects = request.user.members_projects.all()
        context = {
            'projects': projects,
        }
    return render(request, 'projects/index.html', context)

@login_required
def project_top(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        if request.POST.get('delete'):
            current.delete()
        return redirect(project_list)
    else:
        projects = request.user.members_projects.all()
        context = {
            'current': current,
            'projects': projects,
        }
        return render(request, 'projects/top.html', context)

@login_required
def article_manager(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = AddArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.project_id = current
            article.person_in_charge = request.user
            article.created_by = request.user
            article.save()
            path = urlparse(article.url).path
            res = get_analytics_data_eq(path, 6)
            for data in reversed(res):
                Analytics.objects.create(
                    path=data['path'],
                    date=data['date'],
                    session=data['session'],
                    conversion=data['cv'],
                    conversion_rate=data['cvr'],
                    article_id=article
                )
            return redirect(article_manager, project_id=project_id)
        else:
            print('invalid form')
    contents = []
    articles = Article.objects.filter(project_id=project_id).all()
    for article in articles:
        analytic = Analytics.objects.filter(article_id=article.id).order_by().reverse()[:5]
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
                ranking = Ranking.objects.filter(article_id=article,keyword_id=k).order_by('date').reverse()[:5]
                kdata = {
                    "keyword": k.keyword,
                    "volume": k.volume,
                    "ranking": {"1": "-", "2": "-", "3": "-",  "4": "-", "5": "-"},
                    "date": {"1": "-", "2": "-", "3": "-",  "4": "-", "5": "-"},
                    "right_wrong": "-",
                    "ranking_page": "-"
                }
                for i, r in enumerate(ranking):
                    if i == 0:
                        kdata["ranking_page"] = r.ranking_page
                        kdata["right_wrong"] = r.get_right_wrong_display()
                    kdata["ranking"][f"{i + 1}"] = r.ranking
                    kdata["date"][f"{i + 1}"] = r.date
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
    return render(request, 'projects/management.html', context)

@login_required
def project_members(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            new = User.objects.filter(email=email)
            if len(new) > 0:
                current.members.add(new[0])
        elif request.POST.get('member'):
            for k, v in request.POST.items():
                if k == 'member':
                    member = User.objects.filter(email=v)
                    current.members.remove(member[0])
        return redirect(project_members, project_id=project_id)
    members = current.members.all()
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'members': members,
    }
    return render(request, 'projects/members.html', context) 

@login_required
def reports(request, project_id):
    return redirect(report_weekly, project_id=project_id)

def create_report_data(data, regex):
    all = {
        'labels': [],
        'cvrData': [],
        'cvrMax': 100.0,
        'cvrStepSize': 20.0,
        'sessionData': [],
        'sessionMax': 0,
        'sessionStepSize': 0
    }
    channel = {
        'labels': [],
        'directData': [],
        'organicData': [],
        'organicConversion': [],
        'paidData': [],
        'referralData': [],
        'displayData': [],
        'socialData': [],
        'emailData': [],
        'othersData': [],
        'max': 0,
        'stepSize': 0        
    }
    cvrMax = 0.0
    sessionMax = 0
    for d in reversed(data):
        all['labels'].append(d.date.strftime('%m/%d~'))
        all['cvrData'].append(d.conversion_rate)
        all['sessionData'].append(d.session)
        channel['labels'].append(d.date.strftime('%m/%d~'))
        channel['directData'].append(d.direct)
        channel['organicData'].append(d.organic)
        channel['organicConversion'].append(d.organic_conversion)
        channel['paidData'].append(d.paid)
        channel['referralData'].append(d.referral)
        channel['displayData'].append(d.display)
        channel['socialData'].append(d.social)
        channel['emailData'].append(d.email)
        channel['othersData'].append(d.others)
        if d.conversion_rate > cvrMax:
            cvrMax = d.conversion_rate
        if d.session > sessionMax:
            sessionMax = d.session
    if cvrMax > 100.0:
        digits = 10 ** (len(str(int(cvrMax))) - 1)
        all['cvrMax'] = math.ceil(cvrMax / digits) * digits
        all['cvrStepSize'] = all['cvrMax'] / 5
    digits = 10 ** (len(str(int(sessionMax))) - 1)
    all['sessionMax'] = math.ceil(sessionMax / digits) * digits
    all['sessionStepSize'] = all['sessionMax'] / 5
    channel['max'] = all['sessionMax']
    channel['stepSize'] = all['sessionStepSize'] 

    rdata = []
    for r in regex:
        ritem = {
            'regex': r[0].regex,
            'data': {
                'labels': [],
                'cvrData': [],
                'cvrMax': 100.0,
                'cvrStepSize': 20.0,
                'sessionData': [],
                'sessionMax': 0,
                'sessionStepSize': 0
            }
        }
        cvrMax = 0.0
        sessionMax = 0
        for e in reversed(r):
            ritem['data']['labels'].append(e.date.strftime('%m/%d~'))
            ritem['data']['cvrData'].append(e.conversion_rate)
            ritem['data']['sessionData'].append(e.session)
            if e.conversion_rate > cvrMax:
                cvrMax = e.conversion_rate
            if e.session > sessionMax:
                sessionMax = e.session
            if cvrMax > 100.0:
                digits = 10 ** (len(str(int(cvrMax))) - 1)
                ritem['data']['cvrMax'] = math.ceil(cvrMax / digits) * digits
                ritem['data']['cvrStepSize'] = ritem['data']['cvrMax'] / 5
            digits = 10 ** (len(str(int(sessionMax))) - 1)
            ritem['data']['sessionMax'] = math.ceil(sessionMax / digits) * digits
            ritem['data']['sessionStepSize'] = ritem['data']['sessionMax'] / 5
        rdata.append(ritem)

    return {'all': all, 'channel': channel, 'regex': rdata}

@login_required
def report_weekly(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = request.POST.get('regex')
            r = Regex.objects.create(
                regex=regex,
                project_id=current
            )
            data = get_weekly_analytics_data_regex(regex, 12)
            for d in data:
                WeeklyDir.objects.create(
                    regex=r,
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    project_id=current
                )
            data = get_monthly_analytics_data_regex(regex, 12)
            for d in data:
                MonthlyDir.objects.create(
                    regex=r,
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    project_id=current
                )
            return redirect(report_weekly, project_id=project_id)
    regex = Regex.objects.filter(project_id=current)
    rdata = []
    for r in regex:
        rdata.append(WeeklyDir.objects.filter(regex=r).order_by('date').reverse()[:12])
    weekly = WeeklyAll.objects.filter(project_id=project_id).order_by('date').reverse()[:24]
    form = RegexForm()
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'data': create_report_data(weekly, rdata),
        'form': form,
        'type': {'en': 'weekly', 'ja': '週次'}
    }
    return render(request, 'projects/reports.html', context)

@login_required
def report_monthly(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = request.POST.get('regex')
            r = Regex.objects.create(
                regex=regex,
                project_id=current
            )
            data = get_weekly_analytics_data_regex(regex, 24)
            for d in data:
                WeeklyDir.objects.create(
                    regex=r,
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    project_id=current
                )   
            data = get_monthly_analytics_data_regex(regex, 24)
            for d in data:
                MonthlyDir.objects.create(
                    regex=r,
                    date=d['date'],
                    users=d['users'],
                    session=d['session'],
                    conversion=d['cv'],
                    conversion_rate=d['cvr'],
                    page_view=d['pv'],
                    page_view_per_session=d['pvr'],
                    project_id=current
                )            
            return redirect(report_monthly, project_id=project_id)
    regex = Regex.objects.filter(project_id=current)
    rdata = []
    for r in regex:
        rdata.append(MonthlyDir.objects.filter(regex=r).order_by('date').reverse()[:24])
    monthly = MonthlyAll.objects.filter(project_id=current).order_by('date').reverse()[:24]
    form = RegexForm()
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'data': create_report_data(monthly, rdata),
        'form': form,
        'type': {'en': 'monthly', 'ja': '月次'}
    }
    return render(request, 'projects/reports.html', context)

@login_required
def ranking(request, project_id):
    return redirect(ranking_all, project_id=project_id)

@login_required
def ranking_all(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        if request.POST.get('keyword') and request.POST.get('article'): 
            keywords = request.POST.get('keyword')
            article_id = request.POST.get('article')
            article = Article.objects.get(id=article_id)
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
                    article.keywords.add(k)
                else:
                    alst = Article.objects.filter(keywords__keyword=e)
                    if not current in alst:
                        article.keywords.add(klst[0])
            messages.add_message(request, messages.ERROR,
                                 "キーワードを登録しました。")
        else:
            messages.add_message(request, messages.ERROR,
                                 "キーワードの登録に失敗しました。")
    articles = Article.objects.filter(project_id=project_id).all()
    keywords = []
    for article in articles:
        akeywords = article.keywords.all()
        size = len(akeywords)
        if size == 0:
            size = 1
        else:
            for k in akeywords:
                ranking = Ranking.objects.filter(article_id=article,keyword_id=k).order_by('date').reverse()[:6]
                kdata = {
                    "keyword": k.keyword,
                    "volume": k.volume,
                    "ranking": {"1": "-", "2": "-", "3": "-",  "4": "-", "5": "-"},
                    "date": {"1": "-", "2": "-", "3": "-",  "4": "-", "5": "-"},
                    "ranking_page": "-"
                }
                for i, r in enumerate(ranking):
                    if i == 0:
                        kdata["ranking_page"] = r.ranking_page
                    kdata[f"{i + 1}"] = r.ranking
                keywords.append(kdata)
    projects = request.user.members_projects.all()
    articles = Article.objects.filter(project_id=current).all() 
    context = {
        'current': current,
        'projects': projects,
        'articles': articles,
        'keywords': keywords,
    }
    return render(request, 'projects/ranking_all.html', context)