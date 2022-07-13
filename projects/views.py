from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projects.models import Website, Keyword, Project, WebsiteKeywordRelation, ProjectCompetitorRelation
from analytics.models import WeeklyAll, MonthlyAll
from accounts.models import User

from projects.forms import ProjectRegisterForm, ProjectCompetitorForm

from analytics.management.commands.utils.get_all_analytics_data import get_weekly_analytics_data, get_monthly_analytics_data

from analytics.views import create_report_data
from ranking.views import create_score

from rest_framework import viewsets
from rest_framework import permissions
from projects.serializers import KeywordSerializer

from urllib.parse import urlparse
from datetime import date
import math
import re


@login_required
def home(request):
    is_error = False
    if request.method == 'POST':
        form = ProjectRegisterForm(request.POST)
        if form.is_valid():
            domain = request.POST.get('domain')
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
                project = Project.objects.create(
                    name=request.POST.get('name'),
                    website=website,
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
                        project=project
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
                        project=project
                    )
                messages.success(request, 'プロジェクトの登録に成功しました')
        return redirect(home)
    projects = request.user.members_projects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'projects/index.html', context)


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


@login_required
def project_settings(request, project_id):
    current = Project.objects.get(id=project_id)
    form = ProjectCompetitorForm()
    if request.method == 'POST':
        if request.POST.get('email'):
            new = User.objects.get_or_none(email=request.POST.get('email'))
            if new:
                if new in current.members.all():
                    messages.error(request, '既にメンバーに追加済みです')
                else:
                    current.members.add(new)
            else:
                messages.error(request, '存在しないユーザーです')
        elif request.POST.get('domain'):
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
                        registered_by = request.user
                    )
                    existed_k = list(WebsiteKeywordRelation.objects.filter(website=new).values_list('keyword', flat=True))
                    for k in current.website.keywords.all():
                        if k not in existed_k:
                            WebsiteKeywordRelation.objects.create(
                                website=new,
                                keyword=k,
                                registered_by=request.user
                            ) 
                    messages.success(request, '競合サイトの追加に成功しました') 
            else:
                new = Website.objects.create(
                    domain=domain,
                    registered_by=request.user
                )
                ProjectCompetitorRelation.objects.create(
                    project = current,
                    competitor = new,
                    registered_by = request.user
                )
                for k in current.website.keywords.all():
                    WebsiteKeywordRelation.objects.create(
                        website=new,
                        keyword=k,
                        registered_by=request.user
                    ) 
                messages.success(request, '競合サイトの追加に成功しました') 
        elif request.POST.get('member'):
            for k, v in request.POST.items():
                if k == 'member':
                    member = User.objects.get(email=v)
                    current.members.remove(member)
            messages.success(request, 'メンバーを削除しました')
        elif request.POST.get('competitor'):
            for k, v in request.POST.items():
                if k == 'competitor':
                    competitor = Website.objects.get(domain=v)
                    current.competitors.remove(competitor)
                    if not (Project.objects.get_or_none(website=competitor) or ProjectCompetitorRelation.objects.get_or_none(competitor=competitor)):
                        competitor.delete()
            messages.success(request, '競合サイトを削除しました')
        elif request.POST.get('delete'):
            current.delete()
            messages.success(request, 'プロジェクトを削除しました')
            return redirect(home)
        return redirect(project_settings, project_id=project_id)
    members = current.members.all()
    competitors = ProjectCompetitorRelation.objects.filter(project=current)
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'members': members,
        'competitors': competitors,
        'form': form,
    }
    return render(request, 'projects/settings.html', context)


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]