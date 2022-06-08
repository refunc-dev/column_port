from django.core.management.base import BaseCommand, CommandError
from articles.models import Article, Keyword, Ranking

from articles.management.commands.utils.search_all_ranking_browser import launch_driver, search_ranking_browser
from articles.management.commands.utils.search_all_ranking_requests import search_ranking_requests

from urllib.parse import urlparse
import datetime
import re

class Command(BaseCommand):

    def handle(self, *args, **options):
        driver = launch_driver()
        today = datetime.date.today()
        keywords = Keyword.objects.all()
        for keyword in keywords:
            res = search_ranking_browser(driver, keyword.keyword)
            for k, v in res.items():
                setattr(keyword, k, v)
            keyword.updated_at = today
            keyword.save()

            articles = keyword.article_set.all()
            for article in articles:
                domain = urlparse(article.url).netloc
                for i, r in enumerate(res.values()):
                    if r and re.search(domain, r):
                        rw = 'wrong'
                        if urlparse(r).path == urlparse(article.url).path:
                            rw = 'right'
                        Ranking.objects.create(
                            article_id=article,
                            keyword_id=keyword,
                            ranking=i+1,
                            ranking_page=r,
                            date=datetime.date.today(),
                            right_wrong=rw
                        )
                        break
        driver.close()
        driver.quit()