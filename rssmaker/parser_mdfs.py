import datetime
from .DbHandler import Issues

def parser_mdfs(bs_object):
    """
    식품의약품안전처 입법/행정예고를 파싱해 Articles 튜플로 반환합니다.
    """
    articles = ()
    table = bs_object.find('div', {'class': 'bbs_list01'})    
    rows = table.find_all('li')

    for row in reversed(rows):

        num = row.find('div', class_='num')
        title = row.find('a', class_ = 'title')
        author = row.find('p', text=lambda x: x and '담당부서' in x)

        if title and num.get_text(strip=True).isdigit():
            issue = IssuesMdfs(title, author, num.get_text(strip=True))
            if issue.item_guid != "":
                articles += (issue,)

    return articles

class IssuesMdfs(Issues):
    """
    식품의약품안전처 입법/행정예고 게시물 구조를 담는 클래스입니다.
    """
    def __init__(self, _title, _author, _num):
        self.title = "mdfs"
        self.link = "https://www.mfds.go.kr/brd/m_209/list.do"
        self.description = "식품의약품안전처 입법/행정예고"
        main_content = _title.get_text(strip=True)
        self.item_title = _title.get_text(strip=True)
        self.item_link = _title['href']
        self.item_description = ""
        self.item_author = _author.get_text(strip=True).replace('담당부서 | ', '')
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = _num
        return
    