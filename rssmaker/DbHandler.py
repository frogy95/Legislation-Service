import sqlite3

def dict_factory(cursor, row):
    # 딕셔너리 팩토리 함수
    # 커서와 행을 받아서 딕셔너리 형태로 변환하여 반환합니다.
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DbHandler:

    def __init__(self):
        # DbHandler 클래스의 생성자
        # 데이터베이스 연결을 수행하고 테이블을 생성합니다.
        self.conn = sqlite3.connect("hmcdb.db")
        self.conn.row_factory = dict_factory
        self.create_table()

    def insert(self, article):
        # 데이터베이스에 기사(article)를 삽입하는 메서드
        cur = self.conn.cursor()
        sql = """Insert Into rss(title ,link, description, 
        item_title, item_link, item_description, item_author, item_category, item_pubDate, item_guid)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        ret = cur.execute(sql, (article.title, article.link, article.description,
                                article.item_title, article.item_link, article.item_description,
                                article.item_author, article.item_category, article.item_pubDate, article.item_guid))
        self.conn.commit()
        print(ret)

    def get_max_id(self, title):
        # 주어진 제목(title)에 해당하는 가장 큰 item_guid 값을 가져오는 메서드
        cur = self.conn.cursor()
        cur.execute("select item_guid from rss where title = '{0}' order by id desc limit 1;".format(title))
        rows = cur.fetchall()
        if len(rows) > 0:
            max_id = int(rows[0]['item_guid'])
        else:
            max_id = 0
        return max_id

    def create_table(self):
        # 테이블을 생성하는 메서드
        sql = """ CREATE TABLE IF NOT EXISTS rss (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    
                    title text NOT NULL,
                    link text NOT NULL,
                    description text NOT NULL,
                    
                    item_title text NOT NULL,
                    item_link text NOT NULL,
                    item_description text NOT NULL,
                    item_author text NOT NULL,
                    item_category text NOT NULL,
                    item_pubDate text NOT NULL,
                    item_guid text NOT NULL
                ); """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()


class Issues:
    # 기본값을 가지는 Issues 클래스
    title = ""
    link = ""
    description = ""
    item_title = ""
    item_link = ""
    item_description = ""
    item_author = ""
    item_category = ""
    item_pubDate = ""
    item_guid = ""