
import os
import datetime
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

start_date = datetime.date(2016, 7, 26)
end_date = datetime.datetime.today().date()

hashtags = ['23andme', 'precisionmedicine', 'personalizedmedicine', 'GenomicsEngland', 'genomic', 'datasharing']

username = os.environ['USERNAME']
password = os.environ['PASSWORD']

Scraper().scrape(username,password, hashtags, start_date, end_date)
