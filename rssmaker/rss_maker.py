import PyRSS2Gen
import datetime
import sys
import configparser
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from DbHandler import DbHandler
from parser_mohw import parser_mohw_publichearing
from parser_mohw import parser_mohw_law
from parser_nhic import parser_nhic_library

#from uploadToGit import github_api_upload

#BASEPATH = 'd:\\service\\legislation-service\\rss\\'
config = configparser.ConfigParser()
config.read('config.ini')
BASEPATH = config['DEFAULT']['BasePath']

def get_html(url):
    html = urlopen(url)
    bs_object = BeautifulSoup(html, "html.parser")
    return bs_object

def get_html_iframe(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "tbl.default.brd9")))
    except TimeoutException:
        print("TimeoutError")
        driver.quit()            

    return BeautifulSoup(driver.page_source, "html.parser")

def get_filtered_bymaxid(db, title, articles):
    max_id = db.get_max_id(title)
    return filter(lambda x: int(x.item_guid) > max_id, articles)

def get_filtered_bypubdate(db, title, articles):
    max_id = db.get_max_id(title)
    return filter(lambda x: int(x.item_guid) > max_id, articles)

def get_new_articles(db, html, title, getfilter, parser):    
    articles = parser(html)
    return getfilter(db, title, articles)    

def publish_rss(db, title, sender):
    cur = db.conn.cursor()
    
    # DB에서 최신 20개 항목 조회
    cur.execute("select * from rss where title = '{0}' order by id desc limit 20;".format(title))
    
    rss = PyRSS2Gen.RSS2(title='', link='', description='', items=[])

    for row in cur.fetchall():
        if rss.title == "":
            rss.title = sender
            rss.link = row['link']
            rss.lastBuildDate = datetime.datetime.now(datetime.UTC)
            rss.description = row['description']

        item = PyRSS2Gen.RSSItem(
            title=row['item_title'],
            link=row['item_link'],
            description=row['item_description'],
            author=row['item_author'],
            categories=row['item_category'],
            pubDate=row['item_pubDate'],
            guid=row['item_guid']
        )
        rss.items.append(item)

    # UTF-8 인코딩으로 XML 파일 쓰기
    file_name = 'rss_{0}.xml'.format(title)
    file_path = BASEPATH + file_name
    encoding = "utf-8"
    rss.write_xml(open(file_path, 'w', encoding = encoding), encoding)
    #github_api_upload(file_path, file_name, encoding)
    return


def save_crawling_nhic_library(db):
    new_articles = get_new_articles(db, get_html('https://www.nhis.or.kr/nhis/minwon/wbhace10210m01.do'),
                                    'nhic_library',
                                    get_filtered_bymaxid,   
                                    parser_nhic_library)

    return new_articles


def save_crawling_mohw_publichearing(db):
    new_articles = get_new_articles(db, get_html_iframe('https://www.mohw.go.kr/menu.es?mid=a10409030000'),
                                            'publichearing',
                                            get_filtered_bymaxid,
                                            parser_mohw_publichearing)

    return new_articles


def save_crawling_mohw_law(db):
    new_articles = get_new_articles(db, get_html('https://www.mohw.go.kr/law.es?mid=a10409010000'),
                                    'law',
                                    get_filtered_bymaxid,
                                    parser_mohw_law)

    return new_articles


def make_rss():
    db = DbHandler()

    new_articles = ()    
    new_articles += (save_crawling_mohw_publichearing(db), )
    new_articles += (save_crawling_nhic_library(db),)
    new_articles += (save_crawling_mohw_law(db), )

    for articles in new_articles:
        for article in articles:
            db.insert(article)

    publish_rss(db, 'publichearing', 'RSS 뉴스피드- 보건복지부 전자공청회')
    publish_rss(db, 'nhic_library', 'RSS 뉴스피드- 건강보험공단 검진 공지사항')
    publish_rss(db, 'law', 'RSS 뉴스피드- 보건복지부 법령/시행령/시행규칙')
    db.conn.close()


if __name__ == "__main__":
    make_rss()
    sys.exit()
