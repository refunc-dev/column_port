from django.core.management.base import BaseCommand, CommandError

from sessions.models import Regex, WeeklyAll, WeeklyDir
from sessions.management.commands.utils.get_all_analytics_data import validate_account_info, get_weekly_analytics_data
from sessions.management.commands.utils.get_specific_analytics_data import get_weekly_analytics_data_regex

from projects.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for p in projects:
            account_info = [p.account_id, p.property_id, p.view_id]
            status_code = validate_account_info(account_info)
            if not status_code == 0:
                continue
            data = get_weekly_analytics_data(1, account_info)
            for d in data:
                dw = WeeklyAll.objects.get_or_none(project=p,date=d['date'])
                if dw:
                    dw.users=d['users']
                    dw.session=d['session']
                    dw.conversion=d['cv']
                    dw.conversion_rate=d['cvr']
                    dw.page_view=d['pv']
                    dw.page_view_per_session=d['pvr']
                    dw.direct=d['direct']
                    dw.organic=d['organic']
                    dw.organic_conversion=d['organic_conversion']
                    dw.organic_conversion_rate=d['organic_conversion_rate']
                    dw.paid=d['paid']
                    dw.referral=d['referral']
                    dw.display=d['display']
                    dw.social=d['social']
                    dw.email=d['email']
                    dw.others=d['others']
                    dw.save()
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
                        project=p
                    )
            regex = Regex.objects.filter(project=p)
            for r in regex:
                res = get_weekly_analytics_data_regex(r.regex, 1, account_info)
                for data in res:
                    dw = WeeklyDir.objects.get_or_none(project=p,regex=r,date=data['date'])
                    if dw:
                        dw.users=data['users'],
                        dw.session=data['session'],
                        dw.conversion=data['cv'],
                        dw.conversion_rate=data['cvr'],
                        dw.page_view=data['pv'],
                        dw.page_view_per_session=data['pvr'],
                        dw.save()
                    else:
                        WeeklyDir.objects.create(
                            regex=r,
                            date=data['date'],
                            users=data['users'],
                            session=data['session'],
                            conversion=data['cv'],
                            conversion_rate=data['cvr'],
                            page_view=data['pv'],
                            page_view_per_session=data['pvr'],
                            project=p
                        )
        