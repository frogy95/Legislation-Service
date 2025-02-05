import datetime
import re
from .DbHandler import Issues

def parser_mohw_publichearing(bs_object):
    """
    보건복지부 전자공청회 목록을 파싱해 Articles 튜플로 반환합니다.
    """
    articles = ()
    table = bs_object.find('table', {'class': 'tbl default brd9'})    
    rows = table.find_all('tr')

    for row in reversed(rows):
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        issue = IssuesPublichearing(cols)

        if issue.item_guid != "":
            articles += (issue,)

    return articles

class IssuesPublichearing(Issues):
    """
    전자공청회 게시물 구조를 담는 클래스입니다.
    """
    def __init__(self, _link):
        self.title = "publichearing"
        self.link = "https://www.mohw.go.kr/menu.es?mid=a10409030000"
        self.description = "보건복지부 입법/행정예고 전자공청회"
        main_content = _link[2].find('a')
        self.item_title = _link[2].get_text(strip=True)
        self.item_link = f"https://www.epeople.go.kr/cmmn/idea/redirect.do?ideaRegNo={re.search(r'([A-Z0-9]{3}-\d{4}-\d{7})', main_content.get('onclick')).group(1)}"
        self.item_description = f"기간 {_link[3].get_text(strip=True)}"
        self.item_author = _link[3].get_text(strip=True)
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = _link[0].text
        return
    

def parser_mohw_law(bs_object):
    """
    보건복지부 법률/시행령/시행규칙 정보를 파싱해 Articles 튜플로 반환합니다.
    """
    articles = ()
    table = bs_object.find('table', {'class': 'tstyle_list'})
    rows = table.find_all('tr')

    for row in reversed(rows):
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        issue = IssuesLaw(cols)

        if issue.item_guid != "":
            articles += (issue,)

    return articles


class IssuesLaw(Issues):
    """
    법률/시행령/시행규칙 게시물 구조를 담는 클래스입니다.
    """
    def __init__(self, _link):
        self.title = "law"
        self.link = "https://www.mohw.go.kr/menu.es?mid=a10409010000"
        self.description = "보건복지부 법률/시행령/시행규칙"
        main_content = _link[2].find('a')
        self.item_title = _link[2].get_text(strip=True)
        self.item_link = f"https://www.law.go.kr/법령/{self.item_title}"
        self.item_description = f"공포일:{_link[3].get_text(strip=True)}, 시행일:{_link[4].get_text(strip=True)}"
        self.item_author = "보건복지부"
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = re.search(r'MST=(\d+)', main_content.get('href')).group(1)
        return