from django.core.management.base import BaseCommand, CommandError

from ranking.management.commands.utils.search_all_ranking_browser import launch_driver, search_ranking_browser
from ranking.management.commands.utils.search_all_ranking_requests import search_ranking_requests

from projects.models import Keyword, Website
from ranking.models import Ranking, KeywordSerp

from urllib.parse import urlparse
import datetime
import re

class Command(BaseCommand):

    def handle(self, *args, **options):
        driver = launch_driver()
        keywords = Keyword.objects.filter(updated_at__lt=datetime.date.today())
        for keyword in keywords:
            res = search_ranking_browser(driver, keyword.keyword)
            serps = KeywordSerp.objects.create(
                keyword=keyword
            )
            for k, v in res.items():
                setattr(serps, f'url_{k}', v['url'])
                setattr(serps, f'title_{k}', v['title'])
            serps.save()
            keyword.updated_at = datetime.date.today()
            keyword.save()

            websites = keyword.website_set.all()
            for website in websites:
                is_ranked = False
                for k, v in res.items():
                    if v['url'] and re.search(website.domain, v['url']):
                        Ranking.objects.create(
                            website=website,
                            keyword=keyword,
                            ranking=int(k),
                            ranking_page=urlparse(v['url']).path,
                            title_link=v['title'],
                            date=datetime.date.today(),
                        )
                        is_ranked = True
                        break
                if not is_ranked:
                    Ranking.objects.create(
                        website=website,
                        keyword=keyword,
                        ranking=0,
                        ranking_page=None,
                        title_link=None,
                        date=datetime.date.today(),
                    )
        driver.close()
        driver.quit()