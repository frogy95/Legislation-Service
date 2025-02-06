import datetime
from .DbHandler import Issues
from .abstract_parser import parse_items

def parser_mdfs(bs_object):
    """
    식품의약품안전처 입법/행정예고 파서 (추상 로직 적용)
    """
    container = bs_object.find('div', {'class': 'bbs_list01'})
    return parse_items(
        container,
        lambda cont: cont.find_all('li'),
        lambda row: (
            IssuesMdfs(
                row.find('a', class_='title'),
                row.find('p', text=lambda x: x and '담당부서' in x),
                row.find('div', class_='num').get_text(strip=True)
            ) if (row.find('a', class_='title') and row.find('div', class_='num') and row.find('div', class_='num').get_text(strip=True).isdigit())
            else None
        )
    )

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
        self.item_pubDate = datetime.datetime.now(datetime.timezone.utc)
        self.item_guid = _num
        return
