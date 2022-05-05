import os
import re
import csv
import random
import datetime
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException 
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from by_pass_captcha import by_pass_captcha

# Logger setting
#from logging import getLogger, FileHandler, DEBUG
#logger = getLogger(__name__)
#today = datetime.datetime.now()
#os.makedirs('./log', exist_ok=True)
#handler = FileHandler(f'log/{today.strftime("%Y-%m-%d")}_result.log', mode='a')
#handler.setLevel(DEBUG)
#logger.setLevel(DEBUG)
#logger.addHandler(handler)
#logger.propagate = False

### functions ###
def launch_driver():
    url = "https://www.google.co.jp/"

    ua = UserAgent()
#    logger.debug(f'UserAgent: {ua.chrome}\n')

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
#        print([s, str(rank), site_title, site_url, today.strftime('%Y/%m/%d')])
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
def search_ranking_browser(domain, search_words):
    try:
        data = []

        driver = launch_driver()

        for index, search_word in enumerate(search_words):
            logger.info(f'{index + 1} > {search_word}')

            driver.execute_script('''window.open("","_blank");''')
            driver.switch_to.window(driver.window_handles[1])

            # Googleから検索結果ページを取得する
            url = f'https://www.google.co.jp/search?hl=ja&num=100&q={search_word}'
            driver.get(url)

            sleep(random.randint(1, 2))
            if check_exists_by_class_name(driver, 'g-recaptcha'):
#                logger.debug('recaptcha detected\n')
                driver.implicitly_wait(5)
                driver.find_element_by_xpath('//iframe[@title="reCAPTCHA"]').click()
                sleep(random.randint(2, 4))
                ret = by_pass_captcha(driver)
#                if ret == False:
#                    logger.debug("recaptcha failed")

            sleep(random.randint(1, 2))
            if check_exists_by_xpath(driver, '//input[@value="同意する"]'):
                driver.implicitly_wait(5)
                driver.find_element_by_xpath('//input[@value="同意する"]').click()
                sleep(random.randint(2, 4))
            
            # Googleのページ解析を行う
            soup = BeautifulSoup(driver.page_source, "html.parser")

#            logger.debug('【HTMLソース】↓↓↓')
#            logger.debug(f'{soup}')
#            logger.debug('【HTMLソース】↑↑↑\n')

            search_site_list = soup.select('div.ZINbbc.xpd.O9g5cc.uUPGi')

            if domain:
                data.append(search_specific_rank(domain, search_word, search_site_list))
            else:
                data.extend(list(search_all_rank(search_word, search_site_list)))
#            sleep(100)
            sleep(random.randint(2, 5))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        driver.close()
        driver.quit()


    except Exception as err:
#        logger.debug(f'search_ranking: {err}')
        return(1)