from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.decorators import owner_check
from django.shortcuts import render, redirect

from projects.models import Website, Keyword, Project, WebsiteKeywordRelation, ProjectMemberRelation, ProjectCompetitorRelation
from analytics.models import WeeklyAll, MonthlyAll
from accounts.models import User

from projects.forms import ProjectRegisterForm, ProjectCompetitorsForm, ProjectAnalyticsForm

from analytics.management.commands.utils.get_all_analytics_data import validate_account_info, get_weekly_analytics_data, get_monthly_analytics_data

from analytics.views import create_report_data
from ranking.views import create_score

from urllib.parse import urlparse
from datetime import date
import math
import re


def get_analytics_data(request, project, account_info):
    try:
        dataW = get_weekly_analytics_data(24, account_info)
        dataM = get_monthly_analytics_data(24, account_info)
    except Exception as e:
        messages.error(request, '流入データの取得に失敗しました') 
        return
    try:
        for d in dataW:
            data = WeeklyAll.objects.get_or_none(project=project,date=d['date'])
            if data:
                data.users=d['users']
                data.session=d['session']
                data.conversion=d['cv']
                data.conversion_rate=d['cvr']
                data.page_view=d['pv']
                data.page_view_per_session=d['pvr']
                data.direct=d['direct']
                data.organic=d['organic']
                data.organic_conversion=d['organic_conversion']
                data.organic_conversion_rate=d['organic_conversion_rate']
                data.paid=d['paid']
                data.referral=d['referral']
                data.display=d['display']
                data.social=d['social']
                data.email=d['email']
                data.others=d['others']
                data.save()
            else:
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
                    project=project
                )   
        for d in dataM:
            data = MonthlyAll.objects.get_or_none(project=project,date=d['date'])
            if data:
                data.users=d['users']
                data.session=d['session']
                data.conversion=d['cv']
                data.conversion_rate=d['cvr']
                data.page_view=d['pv']
                data.page_view_per_session=d['pvr']
                data.direct=d['direct']
                data.organic=d['organic']
                data.organic_conversion=d['organic_conversion']
                data.organic_conversion_rate=d['organic_conversion_rate']
                data.paid=d['paid']
                data.referral=d['referral']
                data.display=d['display']
                data.social=d['social']
                data.email=d['email']
                data.others=d['others']
                data.save()
            else:
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
                    project=project
                )
    except Exception as e:
        messages.error(request, '流入データの登録に失敗しました') 
        return
    messages.success(request, '流入データの登録に成功しました')


@login_required
def home(request):
    is_error = False
    if request.method == 'POST':
        form = ProjectRegisterForm(request.POST)
        if form.is_valid():
            domain = request.POST.get('domain').strip()
            if re.search(r'//', domain):
                o = urlparse(domain)
                domain = o.hostname
            website = Website.objects.get_or_none(domain=domain)
            if website:
                project = Project.objects.get_or_none(website=website)
                if project:
                    is_error = True
                    messages.error(request, '既に登録済みのドメインです')
            else:
                website = Website.objects.create(
                    domain=domain,
                    registered_by=request.user
                )
            if not is_error:
                account_id = request.POST.get('account_id').strip()
                property_id = request.POST.get('property_id').strip()
                view_id = request.POST.get('view_id').strip()
                project = Project.objects.create(
                    name=request.POST.get('name'),
                    website=website,
                    created_by=request.user,
                    account_id=account_id,
                    property_id=property_id,
                    view_id=view_id
                )
                ProjectMemberRelation.objects.create(
                    project=project,
                    member=request.user,
                    role='admin'
                )
                messages.success(request, 'プロジェクトの登録に成功しました')
                if account_id or property_id or view_id:
                    account_info = [account_id, property_id, view_id]
                    status_code = validate_account_info(account_info)
                    if status_code == 0:
                        get_analytics_data(request, project, account_info)
                    else:
                        if status_code == 1:
                            messages.error(request, 'アカウントにアクセスできません')
                        if status_code == 2:
                            messages.error(request, 'プロパティにアクセスできません')
                        if status_code == 3:
                            messages.error(request, 'ビューにアクセスできません')
        return redirect(home)
    projects = request.user.members_projects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'projects/index.html', context)


@owner_check
@login_required
def project_top(request, project_id):
    current = Project.objects.get(id=project_id)
    projects = request.user.members_projects.all()
    weekly = WeeklyAll.objects.filter(project=current).order_by('date').reverse()[:24]
    context = {
        'current': current,
        'projects': projects,
        'data': create_report_data(weekly, []),
        'score': create_score(current),
        'type': {'en': 'weekly', 'ja': '週次'}
    }
    return render(request, 'projects/top.html', context)


@owner_check
@login_required
def project_settings(request, project_id):
    current = Project.objects.get(id=project_id)
    members = ProjectMemberRelation.objects.filter(project=current)
    competitors = ProjectCompetitorRelation.objects.filter(project=current)
    projects = request.user.members_projects.all()
    role = ProjectMemberRelation.objects.get(project=current,member=request.user).role
    context = {
        'current': current,
        'projects': projects,
        'members': members,
        'competitors': competitors,
        'role': role,
    }
    return render(request, 'projects/settings.html', context)


@owner_check
@login_required
def project_settings_delete(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST' and request.POST.get('delete'):
        current.delete()
        messages.success(request, 'プロジェクトを削除しました')
        return redirect(home)
    return redirect(project_settings, project_id=project_id)


@owner_check
@login_required
def project_settings_analytics(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectAnalyticsForm(request.POST)
        if form.is_valid():
            current.account_id = request.POST.get('account_id').strip()
            current.property_id = request.POST.get('property_id').strip()
            current.view_id = request.POST.get('view_id').strip()
            current.save()
            account_info = [current.account_id, current.property_id, current.view_id]
            status_code = validate_account_info(account_info)
            if status_code == 0:
                get_analytics_data(request, current, account_info)
            else:
                if status_code == 1:
                    messages.error(request, 'アカウントにアクセスできません')
                if status_code == 2:
                    messages.error(request, 'プロパティにアクセスできません')
                if status_code == 3:
                    messages.error(request, 'ビューにアクセスできません')
    return redirect(project_settings, project_id=project_id)


@owner_check
@login_required
def project_settings_members(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST' and request.POST.get('email'):
        new = User.objects.get_or_none(email=request.POST.get('email'))
        if new:
            if new in current.members.all():
                messages.error(request, '既にメンバーに追加済みです')
            else:
                ProjectMemberRelation.objects.create(
                    project=current,
                    member=new,
                    role='member'
                )
        else:
            messages.error(request, '存在しないユーザーです')
    return redirect(project_settings, project_id=project_id)


@owner_check
@login_required
def project_settings_members_delete(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST' and request.POST.get('member'):
        for k, v in request.POST.items():
            if k == 'member':
                member = User.objects.get(email=v)
                current.members.remove(member)
                messages.success(request, 'メンバーを削除しました')
    return redirect(project_settings, project_id=project_id)


@owner_check
@login_required
def project_settings_competitors(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectCompetitorsForm(request.POST)
        if form.is_valid():
            domain = request.POST.get('domain')
            if re.search(r'//', domain):
                o = urlparse(domain)
                domain = o.hostname
            if domain == current.website.domain:
                messages.error(request, 'プロジェクトと同一ドメインです')
                return redirect(project_settings, project_id=project_id)
            new = Website.objects.get_or_none(domain=domain)
            if new:
                if new in current.competitors.all():
                    messages.error(request, '既に競合サイトに追加済みです') 
                else:
                    ProjectCompetitorRelation.objects.create(
                        project = current,
                        competitor = new,
                        name=request.POST.get('name'),
                        registered_by = request.user
                    )
                    existed_k = list(WebsiteKeywordRelation.objects.filter(website=new).values_list('keyword', flat=True))
                    for k in current.website.keywords.all():
                        if k not in existed_k:
                            wk = WebsiteKeywordRelation.objects.create(
                                website=new,
                                keyword=k,
                                registered_by=request.user
                            ) 
                            wk.competitors.add(current)
                    messages.success(request, '競合サイトの追加に成功しました') 
            else:
                new = Website.objects.create(
                    domain=domain,
                    registered_by=request.user
                )
                ProjectCompetitorRelation.objects.create(
                    project = current,
                    competitor = new,
                    name=request.POST.get('name'),
                    registered_by = request.user
                )
                for k in current.website.keywords.all():
                    wk = WebsiteKeywordRelation.objects.create(
                        website=new,
                        keyword=k,
                        registered_by=request.user
                    )
                    wk.competitors.add(current)
                messages.success(request, '競合サイトの追加に成功しました')     
    return redirect(project_settings, project_id=project_id)


@owner_check
@login_required
def project_settings_competitors_delete(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST' and request.POST.get('competitor'):
        for k, v in request.POST.items():
            if k == 'competitor':
                competitor = Website.objects.get(domain=v)
                current.competitors.remove(competitor)
                if not (Project.objects.get_or_none(website=competitor) or ProjectCompetitorRelation.objects.get_or_none(competitor=competitor)):
                    competitor.delete()
                messages.success(request, '競合サイトを削除しました')
    return redirect(project_settings, project_id=project_id)