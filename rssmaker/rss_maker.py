import PyRSS2Gen
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from DbHandler import DbHandler
from parser_mohw import parser_mohw_publichearing
from parser_mohw import parser_mohw_law
from parser_nhic import parser_nhic_library


#BASEPATH = 'd:\\service\\legislation-service\\rss\\'
BASEPATH = 'C:\\Users\\frogy95\\Documents\\GitSources\\Legislation-Service\\rss\\'

def get_new_articles(db, url, title, parser):
    html = urlopen(url)
    bs_object = BeautifulSoup(html, "html.parser")

    articles = parser(bs_object)
    max_id = db.get_max_id(title)

    return filter(lambda x: int(x.item_guid) > max_id, articles)


def publish_rss(db, title, sender):
    cur = db.conn.cursor()

    cur.execute("select * from rss where title = '{0}' order by id desc limit 20;".format(title))

    rss = PyRSS2Gen.RSS2(title='', link='', description='', items=[])

    for row in cur.fetchall():
        if rss.title == "":
            rss.title = sender
            rss.link = row['link']
            rss.lastBuildDate = datetime.datetime.utcnow()
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

    rss.write_xml(open(BASEPATH + 'rss_{0}.xml'.format(title), 'w'), encoding="EUC-KR")


def save_crawling_nhic_library(db):
    new_articles = get_new_articles(db, 'http://sis.nhis.or.kr/ggoz101_r01.do?BLBD_TYPE=00&amp;reqUrl=ggoz101m01',
                                    'nhic_library',
                                    parser_nhic_library)

    return new_articles


def save_crawling_mohw_publichearing(db):
    new_articles = get_new_articles(db, 'https://www.mohw.go.kr/menu.es?mid=a10409030000',
                                    'publichearing',
                                    parser_mohw_publichearing)

    return new_articles


def save_crawling_mohw_law(db):
    new_articles = get_new_articles(db, 'https://www.mohw.go.kr/law.es?mid=a10409010000',
                                    'law',
                                    parser_mohw_law)

    return new_articles


def make_rss():
    db = DbHandler()

    new_articles = ()
    new_articles += (save_crawling_mohw_law(db), )
    #new_articles += (save_crawling_mohw_publichearing(db), )
    #new_articles += (save_crawling_nhic_library(db),)

    for articles in new_articles:
        for article in articles:
            db.insert(article)

    publish_rss(db, 'law', 'RSS 뉴스피드- 보건복지부 법령/시행령/시행규칙')
    #publish_rss(db, 'publichearing', 'RSS 뉴스피드- 보건복지부 전자공청회')
    #publish_rss(db, 'nhic_library', 'RSS 뉴스피드- 건강보험공단 검진 공지사항')
    db.conn.close()


if __name__ == "__main__":
    make_rss()
    quit()