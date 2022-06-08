import os
import re
import csv
import random
import datetime
import urllib.parse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException 
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

from articles.management.commands.utils.by_pass_captcha import by_pass_captcha

### functions ###
def launch_driver():
    url = "https://www.google.co.jp/"

    ua = UserAgent()

    options = Options()
#    options.add_argument('--headless')
    options.add_argument(f'user-agent={ua.chrome}')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    driver.maximize_window()
    return driver

def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

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
    while rank <= 100:
        ranking[f"url_{rank}"] = None
        rank += 1
    return ranking

def search_ranking_browser(driver, kw):
    try:
        # Googleから検索結果ページを取得する
        url = f'https://www.google.co.jp/search?hl=ja&num=100&q={kw}'
        driver.get(url)

        sleep(random.randint(1, 2))
        if check_exists_by_class_name(driver, 'g-recaptcha'):
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//iframe[@title="reCAPTCHA"]').click()
            sleep(random.randint(2, 4))
            ret = by_pass_captcha(driver)
#               if ret == False:
#                   logger.debug("recaptcha failed")

        sleep(random.randint(1, 2))
        if check_exists_by_xpath(driver, '//input[@value="同意する"]'):
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//input[@value="同意する"]').click()
            sleep(random.randint(2, 4))
            
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_site_list = soup.select('div.ZINbbc.xpd.O9g5cc.uUPGi')

        return search_all_rank(search_site_list)

    except Exception as err:
        print(f'search_ranking: {err}')
        return(1)