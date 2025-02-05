import PyRSS2Gen
import datetime
import ssl
import logging
import configparser
import os
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .DbHandler import DbHandler
from .parser_mohw import parser_mohw_publichearing
from .parser_mohw import parser_mohw_law
from .parser_nhic import parser_nhic_library
from .parser_biz_hira import parser_biz_hira
from .parser_mdfs import parser_mdfs
from .response_hira import urlopen_hira


config = configparser.ConfigParser()
config.read('config.ini')
BASEPATH = config['DEFAULT']['BasePath']

def get_bizhira():
    try:
        return urlopen_hira()
    except Exception as e:
        logging.error(f"Error fetching HTML from Hira: {e}")
        return None

def fetch_html(url, use_iframe=False):
    """
    URL을 열어 BeautifulSoup 객체로 반환합니다.
    use_iframe가 True일 경우, Selenium을 이용해 iframe 내부 콘텐츠를 가져옵니다.
    """
    if not use_iframe:
        try:
            context = ssl._create_unverified_context()
            html = urlopen(url, context=context)
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            logging.error(f"Error fetching HTML from {url}: {e}")
            return None
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "tbl.default.brd9")))
        except TimeoutException:
            logging.error(f"TimeoutError fetching iframe from {url}")
        finally:
            page_source = driver.page_source
            driver.quit()

        return BeautifulSoup(page_source, "html.parser")

def get_filtered_bymaxid(db, title, articles):
    max_id = db.get_max_id(title)
    return filter(lambda x: int(x.item_guid) > int(max_id), articles)

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
            rss.lastBuildDate = datetime.datetime.now(datetime.timezone.utc)
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

    file_name = 'rss_{0}.xml'.format(title)
    # BASEPATH 존재 여부 체크 및 fallback 디렉토리 처리
    if not os.path.exists(BASEPATH):
        logging.error(f"Base path {BASEPATH} does not exist. Using './rss' directory instead.")
        fallback_dir = os.path.join(os.getcwd(), "rss")
        if not os.path.exists(fallback_dir):
            os.makedirs(fallback_dir)
        file_path = os.path.join(fallback_dir, file_name)
    else:
        file_path = os.path.join(BASEPATH, file_name)

    # UTF-8 인코딩으로 XML 파일 쓰기
    with open(file_path, 'w', encoding="utf-8") as f:
        rss.write_xml(f, "utf-8")
    return

def save_crawling_biz_hira(db):
    try:
        new_articles = get_new_articles(db, get_bizhira(),
                                        'biz_hira',
                                        get_filtered_bymaxid,   
                                        parser_biz_hira)
        return new_articles
    except Exception as e:
        logging.error(f"Error save_crawling_biz_hira : {e}")
        return None

def save_crawling_nhic_library(db):
    try:
        new_articles = get_new_articles(db, fetch_html('https://www.nhis.or.kr/nhis/minwon/wbhace10210m01.do'),
                                        'nhic_library',
                                        get_filtered_bymaxid,   
                                        parser_nhic_library)
        return new_articles
    except Exception as e:
        logging.error(f"Error save_crawling_nhic_library : {e}")
        return None

def save_crawling_mohw_publichearing(db):
    try:
        new_articles = get_new_articles(db, fetch_html('https://www.mohw.go.kr/menu.es?mid=a10409030000', use_iframe=True),
                                        'publichearing',
                                        get_filtered_bymaxid,
                                        parser_mohw_publichearing)
        return new_articles
    except Exception as e:
        logging.error(f"Error save_crawling_mohw_publichearing : {e}")
        return None

def save_crawling_mohw_law(db):
    try:        
        new_articles = get_new_articles(db, fetch_html('https://www.mohw.go.kr/menu.es?mid=a10409010000'),
                                        'law',
                                        get_filtered_bymaxid,
                                        parser_mohw_law)
        return new_articles
    except Exception as e:
        logging.error(f"Error save_crawling_mohw_law : {e}")
        return None

def save_crawling_mdfs(db):
    try:        
        new_articles = get_new_articles(db, fetch_html('https://www.mfds.go.kr/brd/m_209/list.do'),
                                        'mdfs',
                                        get_filtered_bymaxid,
                                        parser_mdfs)
        return new_articles
    except Exception as e:
        logging.error(f"Error save_crawling_mdfs : {e}")
        return None

def make_rss():
    db = DbHandler()

    new_articles = []   # 리스트로 초기화

    result = save_crawling_mdfs(db)
    if result:
        new_articles.extend(result)

    result = save_crawling_biz_hira(db)
    if result:
        new_articles.extend(result)
    
    result = save_crawling_mohw_publichearing(db)
    if result:
        new_articles.extend(result)
    
    result = save_crawling_nhic_library(db)
    if result:
        new_articles.extend(result)

    result = save_crawling_mohw_law(db)
    if result:
        new_articles.extend(result)

    try:
        for article in new_articles:
            db.insert(article)
    except Exception as e:
        logging.error(f"Error make_rss, dbInsert : {e}")

    publish_rss(db, 'mdfs', 'RSS 뉴스피드- 식품의약품안전처 입법/행정예고')
    publish_rss(db, 'biz_hira', 'RSS 뉴스피드- HIRA 요양기관업무포털 공지사항')
    publish_rss(db, 'publichearing', 'RSS 뉴스피드- 보건복지부 전자공청회')
    publish_rss(db, 'nhic_library', 'RSS 뉴스피드- 건강보험공단 검진 공지사항')
    publish_rss(db, 'law', 'RSS 뉴스피드- 보건복지부 법령/시행령/시행규칙')
    db.conn.close()

