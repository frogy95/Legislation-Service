import datetime
from .DbHandler import Issues
from .abstract_parser import parse_items

def process_line(line):
    if 'N\x1f\x03\x1f' in line:
        header_line = line.split('N\x1f\x03\x1f', 1)[1].strip()
        headers = header_line.split('\x1f')
        if len(headers) in [10, 19]:
            return IssuesBizHira(headers)
    return None

def parser_biz_hira(data):
    data_lines = data.split('\n')
    return parse_items(
        data_lines,
        lambda lines: lines,  # 데이터 라인 그대로 사용
        lambda line: process_line(line)
    )

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
        self.item_pubDate = datetime.datetime.now(datetime.timezone.utc)
        self.item_guid = _link[2] if len(_link) == 10 else _link[11]
        return
