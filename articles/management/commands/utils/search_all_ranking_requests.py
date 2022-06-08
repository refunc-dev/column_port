import os
import re
import csv
import random
import requests
import datetime
import urllib.parse
from time import sleep
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Logger setting
from logging import getLogger, FileHandler, DEBUG
logger = getLogger(__name__)
today = datetime.datetime.now()
os.makedirs('./log', exist_ok=True)
handler = FileHandler(f'log/{today.strftime("%Y-%m-%d")}_result.log', mode='a')
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def search_all_rank(ssl):
    # ページ解析と結果の出力
    ranking = {}
    rank = 1
    for item in ssl:
        try:
            snippet = item.select('div.BNeawe.uEec3.AP7Wnd')[0].text
        except IndexError:
            snippet = None
        try:
            site = item.select('div.egMi0.kCrYT > a')[0]
            try:
                site_title = site.select('h3.zBAuLc')[0].text
            except IndexError:
                site_title = site.select('img')[0]['alt']
        except IndexError:
            if snippet and re.search('強調スニペットについて', snippet):
                site = item.select('div.kCrYT > a')[0]
                site_title = site.select('span.UMOHqf.EDgFbc')[0].text
            else:
                continue
        site_url = site['href']
        parse_result = urllib.parse.urlparse(site_url)
        query = parse_result.query
        dic = urllib.parse.parse_qs(query)
        try:
            ranking[f"url_{rank}"] = dic["url"][0]
        except Exception as err:
            ranking[f"url_{rank}"] = "Unrecognized"
        rank += 1
    return ranking

### main_script ###
def search_ranking_requests(kw):
    try:
        # Googleから検索結果ページを取得する
        ua = UserAgent()
        headers = {"User-Agent": str(ua.chrome)}
        logger.info(ua.chrome)

        url = f'https://www.google.co.jp/search?hl=ja&num=100&q={kw}'
        request = requests.get(url, headers=headers)

        # Googleのページ解析を行う
        soup = BeautifulSoup(request.text, "html.parser")
        search_site_list = soup.select('div.ZINbbc.xpd.O9g5cc.uUPGi')

        return search_all_rank(search_site_list)

    except Exception as err:
        logger.debug(f'search_ranking: {err}')
        exit(1)