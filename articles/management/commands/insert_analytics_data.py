from django.core.management.base import BaseCommand, CommandError
from articles.models import Article, ArticleAnalytics

from articles.management.commands.utils.get_specific_analytics_data import validate_account_info, get_analytics_data_eq

from urllib.parse import urlparse

class Command(BaseCommand):

    def handle(self, *args, **options):
        projects = Project.objects.all()
        for p in projects:
            account_info = [p.account_id, p.property_id, p.view_id]
            status_code = validate_account_info(account_info)
            if not status_code == 0:
                continue
            articles = p.article_set.all()
            for article in articles:
                path = urlparse(article.url).path
                res = get_analytics_data_eq(path, 1, account_info)
                for data in res:
                    da = ArticleAnalytics.objects.get_or_none(article=article,date=data['date'])
                    if da:
                        da.session = data['session'],
                        da.conversion = data['cv'],
                        da.conversion_rate = data['cvr'],
                        da.save()
                    else:
                        ArticleAnalytics.objects.create(
                            article=article
                            date=data['date'],
                            session=data['session'],
                            conversion=data['cv'],
                            conversion_rate=data['cvr']
                        )