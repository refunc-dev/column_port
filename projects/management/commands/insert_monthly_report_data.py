from django.core.management.base import BaseCommand, CommandError
from projects.models import Project, Regex, Monthly
from projects.management.commands.utils.get_specific_analytics_data import get_monthly_analytics_data_regex


class Command(BaseCommand):

    def handle(self, *args, **options):
        projects = Porject.objects.all()
        for p in projects:
            regex = Regex.objects.filter(project_id=p.id)
            for r in regex:
                res = get_monthly_analytics_data_regex(r.regex, 1)
                for data in res:
                    Monthly.objects.create(
                        regex=data['regex'],
                        year_month=data['term'],
                        session=data['session'],
                        conversion=data['cv'],
                        conversion_rate=data['cvr'],
                        page_view=data['pv'],
                        page_view_per_session=data['pvr'],
                        project_id=r.project_id
                    )