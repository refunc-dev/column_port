from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.decorators import owner_check
from django.shortcuts import render, redirect

from analytics.models import Regex, WeeklyAll, MonthlyAll, WeeklyDir, MonthlyDir
from analytics.forms import RegexForm

from analytics.management.commands.utils.get_all_analytics_data import get_weekly_analytics_data, get_monthly_analytics_data
from analytics.management.commands.utils.get_specific_analytics_data import get_weekly_analytics_data_regex, get_monthly_analytics_data_regex

from projects.models import Project
from accounts.models import User

from datetime import date
import math
import re


def define_step_size(max):
    chunk = math.ceil(math.ceil(max) / 5)
    digits = 10 ** (len(str(int(chunk))) - 1)
    return math.ceil(chunk / digits) * digits


def create_report_data(data, regex, report_type='weekly'):
    all = {
        'labels': [],
        'cvrData': [],
        'cvrMax': 0.0,
        'cvrStepSize': 0.0,
        'sessionData': [],
        'sessionMax': 0,
        'sessionStepSize': 0,
        'cvData': [],
        'cvMax': 0,
        'cvStepSize': 0
    }
    organic = {
        'labels': [],
        'cvrData': [],
        'cvrMax': 0.0,
        'cvrStepSize': 0.0,
        'sessionData': [],
        'sessionMax': 0,
        'sessionStepSize': 0,
        'cvData': [],
        'cvMax': 0,
        'cvStepSize': 0
    }
    channel = {
        'labels': [],
        'directData': [],
        'organicData': [],
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
    cvMax = 0
    organicCvrMax = 0.0
    organicSessionMax = 0
    organicCvMax = 0
    channelSessionMax = 0
    for d in reversed(data):
        if report_type == 'monthly':
            all['labels'].append(d.date.strftime('%-y年%-m月'))
            organic['labels'].append(d.date.strftime('%-y年%-m月'))
            channel['labels'].append(d.date.strftime('%-y年%-m月'))
        else:
            all['labels'].append(d.date.strftime('%-m/%-d~'))
            organic['labels'].append(d.date.strftime('%-m/%-d~'))
            channel['labels'].append(d.date.strftime('%-m/%-d~'))
        all['cvrData'].append(d.conversion_rate)
        all['sessionData'].append(d.session)
        all['cvData'].append(d.conversion)
        cvrMax = max(d.conversion_rate, cvrMax)
        sessionMax = max(d.session, sessionMax)
        cvMax = max(d.conversion, cvMax)
        organic['cvrData'].append(d.organic_conversion_rate)
        organic['sessionData'].append(d.organic)
        organic['cvData'].append(d.organic_conversion)
        organicCvrMax = max(d.organic_conversion_rate, organicCvrMax)
        organicSessionMax = max(d.organic, organicSessionMax)
        organicCvMax = max(d.organic_conversion, organicCvMax)
        channel['directData'].append(d.direct)
        channel['organicData'].append(d.organic)
        channel['paidData'].append(d.paid)
        channel['referralData'].append(d.referral)
        channel['displayData'].append(d.display)
        channel['socialData'].append(d.social)
        channel['emailData'].append(d.email)
        channel['othersData'].append(d.others)
        channelSessionMax = max(d.direct, d.organic, d.paid, d.referral, d.display, d.social, d.email, d.others, channelSessionMax)
    all['cvrStepSize'] = define_step_size(cvrMax)
    all['cvrMax'] = all['cvrStepSize'] * 5
    all['sessionStepSize'] = define_step_size(sessionMax)
    all['sessionMax'] = all['sessionStepSize'] * 5
    all['cvStepSize'] = define_step_size(cvMax)
    all['cvMax'] = all['cvStepSize'] * 5
    organic['cvrStepSize'] = define_step_size(organicCvrMax)
    organic['cvrMax'] = organic['cvrStepSize'] * 5
    organic['sessionStepSize'] = define_step_size(organicSessionMax)
    organic['sessionMax'] = organic['sessionStepSize'] * 5
    organic['cvStepSize'] = define_step_size(organicCvMax)
    organic['cvMax'] = organic['cvStepSize'] * 5
    channel['stepSize'] = define_step_size(channelSessionMax)
    channel['max'] = channel['stepSize'] * 5

    rdata = []
    for r in regex:
        ritem = {
            'regex': r[0].regex,
            'data': {
                'labels': [],
                'cvrData': [],
                'cvrMax': 0.0,
                'cvrStepSize': 0.0,
                'sessionData': [],
                'sessionMax': 0,
                'sessionStepSize': 0
            }
        }
        cvrMax = 0.0
        sessionMax = 0
        for e in reversed(r):
            if report_type == 'monthly':
                ritem['data']['labels'].append(e.date.strftime('%-y年%-m月'))
            else:
                ritem['data']['labels'].append(e.date.strftime('%-m/%-d~'))
            ritem['data']['cvrData'].append(e.conversion_rate)
            ritem['data']['sessionData'].append(e.session)
            cvrMax = max(e.conversion_rate, cvrMax)
            sessionMax = max(e.session, sessionMax)
        ritem['data']['cvrStepSize'] = define_step_size(cvrMax)
        ritem['data']['cvrMax'] = ritem['data']['cvrStepSize'] * 5
        ritem['data']['sessionStepSize'] = define_step_size(sessionMax)
        ritem['data']['sessionMax'] = ritem['data']['sessionStepSize'] * 5
        rdata.append(ritem)

    return {'all': all, 'organic': organic, 'channel': channel, 'regex': rdata}


def common_process(request, project_id, report_type):
    current = Project.objects.get(id=project_id)
    regex = Regex.objects.filter(project=current).order_by('order')
    rdata = []
    if report_type == 'weekly':
        for r in regex:
                rdata.append(WeeklyDir.objects.filter(regex=r).order_by('date').reverse()[:12])
        term = WeeklyAll.objects.filter(project=current).order_by('date').reverse()[:24]
        ja = '週次'
    elif report_type == 'monthly':
        for r in regex:
            rdata.append(MonthlyDir.objects.filter(regex=r).order_by('date').reverse()[:24])
        term = MonthlyAll.objects.filter(project=current).order_by('date').reverse()[:24]
        ja = '月次'
    form = RegexForm()
    projects = request.user.members_projects.all()
    context = {
        'current': current,
        'projects': projects,
        'data': create_report_data(term, rdata, report_type),
        'form': form,
        'type': {'en': report_type, 'ja': ja}
    }
    return render(request, 'analytics/reports.html', context)


@owner_check
@login_required
def analytics_top(request, project_id):
    return redirect(analytics_weekly, project_id=project_id)


@owner_check
@login_required
def analytics_weekly(request, project_id):
    return common_process(request, project_id=project_id, report_type='weekly')


@owner_check
@login_required
def analytics_monthly(request, project_id):
    return common_process(request, project_id=project_id, report_type='monthly')


@owner_check
@login_required
def regex_add(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = request.POST.get('regex')
            rlist = Regex.objects.filter(project=current).values('regex')
            r = Regex.objects.create(
                regex=regex,
                name=request.POST.get('name'),
                order=len(rlist) + 1,
                project=current,
                created_by=request.user
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
                    project=current
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
                    project=current
                )
            messages.success(request, '正規表現の登録に成功しました')
        else:
            messages.success(request, '正規表現の登録に失敗しました')
        if request.POST.get('type') == 'weekly':
            return redirect(analytics_weekly, project_id=project_id)
        elif request.POST.get('type') == 'monthly':
            return redirect(analytics_monthly, project_id=project_id)
    return redirect(analytics_top, project_id=project_id)


@owner_check
@login_required
def regex_settings(request, project_id):
    current = Project.objects.get(id=project_id)
    if request.method == 'POST':
        for k, v in request.POST.items():
            if re.match(r'order_', k):
                r = Regex.objects.get(id=k.replace('order_',''))
                r.order = v
                r.save()
        idlist = request.POST.getlist('delete')
        rlist = Regex.objects.filter(id__in=idlist)
        for r in rlist:
            r.delete()
        if request.POST.get('type') == 'weekly':
            return redirect(analytics_weekly, project_id=project_id)
        elif request.POST.get('type') == 'monthly':
            return redirect(analytics_monthly, project_id=project_id)
    return redirect(analytics_top, project_id=project_id)