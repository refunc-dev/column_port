from django.core.management.base import BaseCommand, CommandError
from projects.models import Project, Regex, Weekly
from projects.management.commands.utils.get_all_analytics_data import get_weekly_analytics_data
from projects.management.commands.utils.get_specific_analytics_data import get_weekly_analytics_data_regex


class Command(BaseCommand):

    def handle(self, *args, **options):
        projects = Porject.objects.all()
        for p in projects:
            data = get_weekly_analytics_data()
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
                    project_id=r.project_id
                )
            regex = Regex.objects.filter(project_id=p.id)
            for r in regex:
                res = get_weekly_analytics_data_regex(r.regex, 1)
                for data in res:
                    WeeklyDir.objects.create(
                        regex=data['regex'],
                        date=data['date'],
                        users=data['users'],
                        session=data['session'],
                        conversion=data['cv'],
                        conversion_rate=data['cvr'],
                        page_view=data['pv'],
                        page_view_per_session=data['pvr'],
                        project_id=r.project_id
                    )
        