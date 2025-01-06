from DbHandler import Issues
import datetime
import re

def parser_biz_hira(data):
    articles = ()
    data_lines = data.split('\n')
    for line in data_lines:
        if 'N\x1f\x03\x1f' in line:
            header_line = line.split('N\x1f\x03\x1f', 1)[1].strip()
            headers = header_line.split('\x1f')

            if len(headers) in [10, 19]:
                issue = IssuesBizHira(headers)
                if issue.item_guid != "":
                    articles += (issue,)

    return articles

class IssuesBizHira(Issues):
    def __init__(self, _link):
        self.title = "biz_hira"
        self.link = "https://biz.hira.or.kr/index.do"
        self.description = "HIRA 요양기관 업무포털"
        self.item_title = _link[8] if len(_link) == 10 else _link[17]
        self.item_link = ""
        self.item_description = ""
        self.item_author = _link[6] if len(_link) == 10 else _link[15]
        self.item_category = ""
        self.item_pubDate = datetime.datetime.now(datetime.UTC)
        self.item_guid = _link[2] if len(_link) == 10 else _link[11]
        return
