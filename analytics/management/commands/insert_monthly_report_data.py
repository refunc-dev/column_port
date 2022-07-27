from django.core.management.base import BaseCommand, CommandError

from analytics.models import Regex, MonthlyAll, MonthlyDir
from analytics.management.commands.utils.get_all_analytics_data import validate_account_info, get_monthly_analytics_data
from analytics.management.commands.utils.get_specific_analytics_data import get_monthly_analytics_data_regex

from projects.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for p in projects:
            account_info = [p.account_id, p.property_id, p.view_id]
            status_code = validate_account_info(account_info)
            if not status_code == 0:
                continue
            data = get_monthly_analytics_data(1, account_info)
            for d in data:
                dm = MonthlyAll.objects.get_or_none(project=p,date=d['date'])
                if dm:
                    dm.users=d['users']
                    dm.session=d['session']
                    dm.conversion=d['cv']
                    dm.conversion_rate=d['cvr']
                    dm.page_view=d['pv']
                    dm.page_view_per_session=d['pvr']
                    dm.direct=d['direct']
                    dm.organic=d['organic']
                    dm.organic_conversion=d['organic_conversion']
                    dm.organic_conversion_rate=d['organic_conversion_rate']
                    dm.paid=d['paid']
                    dm.referral=d['referral']
                    dm.display=d['display']
                    dm.social=d['social']
                    dm.email=d['email']
                    dm.others=d['others']
                    dm.save()
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
                        project=p
                    )
            regex = Regex.objects.filter(project=p)
            for r in regex:
                res = get_monthly_analytics_data_regex(r.regex, 1, account_info)
                for data in res:
                    dm = MonthlyDir.objects.get_or_none(project=p,regex=r,date=data['date'])
                    if dm:
                        dm.users=data['users'],
                        dm.session=data['session'],
                        dm.conversion=data['cv'],
                        dm.conversion_rate=data['cvr'],
                        dm.page_view=data['pv'],
                        dm.page_view_per_session=data['pvr'],
                        dm.save()
                    else:
                        MonthlyDir.objects.create(
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