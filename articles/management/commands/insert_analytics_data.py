from django.core.management.base import BaseCommand, CommandError
from articles.models import Article, Analytics

from articles.management.commands.utils.get_specific_analytics_data import get_analytics_data_eq

from urllib.parse import urlparse

class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.all()
        for article in articles:
            path = urlparse(article.url).path
            res = get_analytics_data_eq(path, 1)
            for data in res:
                Analytics.objects.create(
                    path=data['path'],
                    date=data['date'],
                    session=data['session'],
                    conversion_rate=data['cvr'],
                    conversion=data['cv'],
                    article_id=article
                )