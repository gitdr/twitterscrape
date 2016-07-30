from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import random
import datetime
from date_generator import DateGenerator
import logging
import time
import os
import pprint

class Scraper:

  def __init__(self):
    self.log = logging.getLogger('twitterscrape.scraper')

  def test_log(self, str):
    self.log.info(str)

  def driver(self):
    return webdriver.Remote(
                  command_executor='http://127.0.0.1:4444/wd/hub',
                  desired_capabilities=DesiredCapabilities.FIREFOX)

  def check_exists_by_xpath(self, driver, xpath):
    try:
      driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
      return False
    return True

  def scrape_session(self, username, password, search_string):

    driver = self.driver()
    
    driver.get("http://www.twitter.com")
    assert "Twitter" in driver.title

    # click login button on the main page
    driver.find_element_by_xpath("//*[@id='doc']/div[1]/div/div[1]/div[2]/a[3]").click()

    # type username
    driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/div[1]/input").send_keys(username)

    # type password
    driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/div[2]/input").send_keys(password)

    # click login button
    driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/input[1]").click()

    if self.check_exists_by_xpath(driver, "//*[@id='signout-button']/button"):
      self.log.info('successfully logged in')
    else:
      self.log.fatal('failed to login')

    # locate and clear main search field
    search_field = driver.find_element_by_xpath("//*[@id='search-query']")
    search_field.clear()
    
    # type search string
    search_field.send_keys(search_string)

    # click search button
    driver.find_element_by_xpath("//*[@id='global-nav-search']/span/button").click()

    self.log.debug("sleeping for 5 secs")
    self.delay()

    # find ol(ordered list) tag container
    ol_element = driver.find_element_by_xpath("//*[@id='stream-items-id']")

    # count number of tweets on page load
    last_num_tweets = len(ol_element.find_elements_by_xpath("*"))
    self.log.info("initial number of tweets: {}".format(last_num_tweets))

    while True:
      self.log.debug("scrolling")
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      self.delay()
      
      # find ol(ordered list) tag container
      element = driver.find_element_by_xpath("//*[@id='stream-items-id']")
      num_tweets = len(element.find_elements_by_xpath("*")) 
      self.log.info("number of tweets during this cycle: {}".format(num_tweets))

      if num_tweets == last_num_tweets:
        self.log.info("last cycles tweets number equal to curreny cycle; breaking")
        break
      else:
        last_num_tweets = num_tweets
        self.log.info("continuing to fetch tweets")

    html = driver.page_source
    driver.close()
    return html

  def delay(self):
    delay = int(abs(np.random.normal(0, 1)) * 2 + 4)
    self.log.debug("sleeping for %i secs" % (delay))
    time.sleep(5)

  def generate_search_string(self, hashtag, date):
    return "%s since:%s until:%s" % (hashtag, date.strftime("%Y-%m-%d"), (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

  def create_combos(self, hashtags, dates):
    result = []

    for ht in hashtags:
      for date in dates:
        result.append([ht, date])

    return result

  def create_base_data_dir(self):
    self.basedir = './data'

    if not os.path.exists(self.basedir):
      os.makedirs(self.basedir)

  def dates(self, start_date, end_date):
    return DateGenerator().generate_dates_in_random_order(start_date, end_date)

  def path(self, hashtag, date):
    return '/'.join([self.basedir, hashtag, date.strftime("%y-%m-%d")])

  def handle_directory(self, path):
    if not os.path.exists(path):
      os.makedirs(path)
      return True;
    
    if os.listdir(path) == []: 
      return True;

    return False;

  def write_file(self, path, data):
    f = open(path, 'w')

    f.write(data.encode('utf8'))

    f.close()

  def scrape(self, username, password, hashtags, start_date, end_date):
    self.create_base_data_dir()
    
    random.shuffle(hashtags)

    # list of all possible combinations of hashtags with dates
    combos = self.create_combos(hashtags, self.dates(start_date, end_date))

    # shuffle the list
    random.shuffle(combos)

    for tuple in combos:

      path = self.path(tuple[0], tuple[1])

      if self.handle_directory(path):
        # data = 'fdsaf'
        data = self.scrape_session(username, password, self.generate_search_string(tuple[0], tuple[1]))
        self.write_file(path + '/data', data)
        self.delay()
