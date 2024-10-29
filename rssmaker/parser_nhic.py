from DbHandler import Issues
import datetime

def parser_nhic_library(bs_object):
    articles = ()
    table = bs_object.body.find('table', summary='게시판')
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
    def __init__(self, _link):
        self.title = "nhic_library"
        self.link = ""
        self.description = "건강보험공단 검진 공지사항"
        main_content = _link[1].find('a')
        self.item_title = _link[1].text.strip('\r').strip('\n').strip('\t').strip()
        self.item_link = "http://sis.nhis.or.kr/ggoz101_r03.do?ITF_TYPE=R&ARTI_NO={0}&BLBD_TYPE2={1}".format(main_content.get('onclick')[21:25], '00')
        self.item_description = "공지일자: {0}".format(_link[3].text)
        self.item_author = _link[2].text.strip('\r').strip('\n').strip('\t').strip()
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.timezone.utc)
        self.item_guid = main_content.get('onclick')[21:25]
        return
