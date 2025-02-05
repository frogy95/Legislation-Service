import logging
from rssmaker.rss_maker import make_rss

def main():
    """RSS 생성 실행 함수"""
    try:
        make_rss()
    except Exception as e:
        logging.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()
