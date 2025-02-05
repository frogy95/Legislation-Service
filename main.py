import logging
import sys
from rssmaker import make_rss

if __name__ == "__main__":
    try:        
        make_rss()
    except Exception as e:
        logging.error(f"Error main : {e}")
    finally:
        sys.exit()
