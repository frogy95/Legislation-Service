from DbHandler import Issues
import datetime
import re

def parser_mohw_publichearing(bs_object):
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
    def __init__(self, _link):
        self.title = "publichearing"
        self.link = "https://www.mohw.go.kr/menu.es?mid=a10409030000"
        self.description = "보건복지부 입법/행정예고 전자공청회"
        main_content = _link[2].find('a')
        self.item_title = _link[2].text.strip('\r').strip('\n').strip('\t').strip()
        self.item_link = "https://www.epeople.go.kr/cmmn/idea/redirect.do?ideaRegNo={0}".format(re.search(r"([A-Z0-9]{3}-\d{4}-\d{7})", main_content.get('onclick')).group(1))        
        self.item_description = "기간 {0}".format(_link[3].text)
        self.item_author = _link[3].text.strip('\r').strip('\n').strip('\t').strip()
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = _link[0].text
        return
    

def parser_mohw_law(bs_object):
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
    def __init__(self, _link):
        self.title = "law"
        self.link = "https://www.mohw.go.kr/board.es?mid=a10409020000&bid=0026"
        self.description = "보건복지부 훈령/예규/고시/지침"
        main_content = _link[2].find('a')
        self.item_title = _link[2].text.strip('\r').strip('\n').strip('\t').strip()
        #self.item_link = main_content.get('href')
        self.item_link = "https://www.law.go.kr/법령/{0}".format(self.item_title)
        self.item_description = "공포일:{0}, 시행일:{1}".format(_link[3].text.strip('\r').strip('\n').strip('\t').strip(), _link[4].text.strip('\r').strip('\n').strip('\t').strip())
        self.item_author = "보건복지부"
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = ''.join(filter(str.isdigit, _link[1].text))
        return