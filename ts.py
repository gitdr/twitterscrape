import logging
import sys
from scraper import Scraper
from parser import Parser

logging.basicConfig(
  stream=sys.stdout,
  format='%(asctime)s %(levelname)s: %(name)s: %(message)s',
  datefmt='%m/%d/%Y %H:%M:%S',
  level=logging.DEBUG)

log = logging.getLogger('twitterscrape')

Scraper().test_log("ksdjfksajfskjd")
Parser().test_log("ksdjfksajfskjd")