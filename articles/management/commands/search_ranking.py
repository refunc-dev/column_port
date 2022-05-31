from django.core.management.base import BaseCommand, CommandError
from articles.models import Article, Keyword, Ranking

from articles.management.commands.utils.search_ranking_browser import search_ranking_browser
from articles.management.commands.utils.search_ranking_requests import search_ranking_requests

from urllib.parse import urlparse

class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = Article.objects.all()
        for article in articles:
            keywords = Keyword.objects.filter(article_id=article.id).all()
            lst = []
            for keyword in keywords:
                e = {"id": keyword.id, "kw": keyword.keyword}
                lst.append(e)
            if len(lst) != 0:
                domain = urlparse(article.url).netloc
                data = search_ranking_browser(domain, lst)
                for r in data:
                    if r == None:
                        continue
                    rw = 'wrong'
                    if urlparse(r[2]).path == urlparse(article.url).path:
                        rw = 'right'
                    Ranking.objects.create(
                        ranking=r[1], 
                        ranking_page=r[2],
                        date=r[3],
                        right_wrong=rw,
                        keyword_id=Keyword.objects.get(id=r[0])
                    )