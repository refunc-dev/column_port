from django.core.management.base import BaseCommand, CommandError
from articles.models import Article, Keyword, Ranking

from search_ranking_browser import search_ranking_browser

class Command(BaseCommand):

    def handle(self, *args, **options):
        ua = UserAgent()
        headers = {"User-Agent": str(ua.chrome)}

        keywords = Keyword.objects.all()
        for keyword in keywords:
