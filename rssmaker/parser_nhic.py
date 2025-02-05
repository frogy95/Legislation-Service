import datetime
import re
from .DbHandler import Issues

def parser_nhic_library(bs_object):
    """
    국민건강보험공단 공지사항을 파싱해 Articles 튜플로 반환합니다.
    """
    articles = ()
    table = bs_object.body.find('table', {'class': 'board-table'})
    rows = table.find_all('tr')

    for row in reversed(rows):
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        issue = IssuesNhicLibrary(cols)

        if issue.item_guid != "":
            articles += (issue,)

    return articles

class IssuesNhicLibrary(Issues):
    """
    국민건강보험공단 소식 구조를 담는 클래스입니다.
    """
    def __init__(self, _link):
        self.title = "nhic_library"
        self.link = "https://www.nhis.or.kr/nhis/minwon/wbhace10210m01.do"
        self.description = "건강보험공단 검진 공지사항"
        main_content = _link[1].find('a')
        self.item_title = _link[1].get_text(strip=True)
        self.item_link = f"https://www.nhis.or.kr/nhis/minwon/wbhace10210m01.do{main_content.get('href')}"
        self.item_description = f"공지일자: {_link[3].get_text(strip=True)}"
        self.item_author = _link[2].get_text(strip=True)
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = re.search(r"articleNo=(\d+)", main_content.get('href')).group(1)
        return
