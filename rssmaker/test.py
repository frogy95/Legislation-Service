from time import sleep
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Set the URL
url = "https://www.mohw.go.kr/menu.es?mid=a10409030000"
urlopen(url)

sleep(5)

url = "https://www.epeople.go.kr/frm/thk/elecPblntcList.npaid?frmMenuMngNo=WBF-1003-000015#"
html_content = urlopen(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(html_content, 'html.parser')

# iframe 내의 HTML 데이터 출력
print(soup.prettify())