import logging
from .rss_maker import make_rss

# 로그 설정
logging.basicConfig(
    level=logging.ERROR, 
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('rss_maker.log')
    ]
    )
