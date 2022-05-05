import os
import re
import csv
import random
import requests
import datetime
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
def create_csv_file(data, outputFilePath):
    header = ["キーワード","順位","タイトル","URL","日付"]
    with open(outputFilePath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\r\n',  quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(data)

def search_all_rank(s, ssl):
    # ページ解析と結果の出力
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
        site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        print([s, str(rank), site_title, site_url, today.strftime('%Y/%m/%d')])
        yield [s, str(rank), site_title, site_url, today.strftime('%Y/%m/%d')]
        rank += 1

def search_specific_rank(d, s, ssl):
    # ページ解析と結果の出力
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
        site_url = site['href'].replace('/url?q=', '')
        # URLにドメインが含まれていたら結果を返す
        if re.search(d, site_url):
            return [s, str(rank), site_title, site_url, today.strftime('%Y/%m/%d')]
    return None

### main_script ###
def search_ranking_requests(domain, search_words):
    try:
        data = []

        for index, search_word in enumerate(search_words):
            logger.info(f'{index + 1} > {search_word}')

            # Googleから検索結果ページを取得する
            ua = UserAgent()
            headers = {"User-Agent": str(ua.chrome)}
            logger.info(ua.chrome)

            url = f'https://www.google.co.jp/search?hl=ja&num=100&q={search_word}'
            request = requests.get(url, headers=headers)

            # Googleのページ解析を行う
            soup = BeautifulSoup(request.text, "html.parser")

            logger.debug('【HTMLソース】↓↓↓')
            logger.debug(soup)
            logger.debug('【HTMLソース】↑↑↑\n')

            search_site_list = soup.select('div.ZINbbc.xpd.O9g5cc.uUPGi')

            if domain:
                data.append(search_specific_rank(domain, search_word, search_site_list))
            else:
                data.extend(list(search_all_rank(search_word, search_site_list)))
            sleep(random.randint(2, 7))
        
        create_csv_file(data, './csv/test.csv')
    except Exception as err:
        logger.debug(f'search_ranking: {err}')
        exit(1)