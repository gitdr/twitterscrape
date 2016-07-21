from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import logging
import time

class Scraper:

  def __init__(self):
    self.log = logging.getLogger('twitterscrape.scraper')

    self.driver = webdriver.Remote(
                    command_executor='http://127.0.0.1:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.FIREFOX)

  def test_log(self, str):
    self.log.info(str)

  def check_exists_by_xpath(self, xpath):
    try:
      self.driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
      return False
    return True

  def scrape(self, parser, username, password, hashtag=None, start_date=None, end_date=None):
    self.driver.get("http://www.twitter.com")
    assert "Twitter" in self.driver.title

    # click login button on the main page
    self.driver.find_element_by_xpath("//*[@id='doc']/div[1]/div/div[1]/div[2]/a[3]").click()

    # type username
    self.driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/div[1]/input").send_keys(username)

    # type password
    self.driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/div[2]/input").send_keys(password)

    # click login button
    self.driver.find_element_by_xpath(
      "//*[@id='login-dialog-dialog']/div[2]/div[2]/div[2]/form/input[1]").click()

    if self.check_exists_by_xpath("//*[@id='signout-button']/button"):
      self.log.info('successfully logged in')
    else:
      self.log.fatal('failed to login')

    # locate and clear main search field
    search_field = self.driver.find_element_by_xpath("//*[@id='search-query']")
    search_field.clear()
    
    # type search string
    search_field.send_keys("#23andme since:2016-06-20 until:2016-07-21")

    # click search button
    self.driver.find_element_by_xpath("//*[@id='global-nav-search']/span/button").click()

    self.log.debug("sleeping for 5 secs")
    time.sleep(5)

    # find ol(ordered list) tag container
    ol_element = self.driver.find_element_by_xpath("//*[@id='stream-items-id']")

    # count number of tweets on page load
    last_num_tweets = len(ol_element.find_elements_by_xpath("*"))
    self.log.info("initial number of tweets: {}".format(last_num_tweets))

    while True:
      self.log.debug("scrolling")
      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      self.log.debug("sleeping for 5 secs")
      time.sleep(5)
      
      # find ol(ordered list) tag container
      element = self.driver.find_element_by_xpath("//*[@id='stream-items-id']")
      num_tweets = len(element.find_elements_by_xpath("*")) 
      self.log.info("number of tweets during this cycle: {}".format(num_tweets))

      if num_tweets == last_num_tweets:
        self.log.info("last cycles tweets number equal to curreny cycle; breaking")
        break
      else:
        last_num_tweets = num_tweets
        self.log.info("continuing to fetch tweets")

    #parser.test_log("ksdjfksajfskjd")

    self.driver.close()

    #pprint.pprint(vars(element))
    #pprint.pprint (dir(element))
    #pprint.pprint (element.text)
    #pprint.pprint(element)
    # raw_input("Press Enter to continue...")
    #elem = driver.find_element_by_name("q")
    #elem.send_keys("pycon")
    #elem.send_keys(Keys.RETURN)
    #assert "No results found." not in driver.page_source
    #pprint.pprint(driver.page_source)