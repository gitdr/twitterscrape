from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import logging

class Scraper:

  def __init__(self):
    self.log = logging.getLogger('twitterscrape.scraper')

    self.driver = webdriver.Remote(
                    command_executor='http://127.0.0.1:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.FIREFOX)

  def test_log(self, str):
    self.log.info(str)

  def check_exists_by_xpath(xpath):
    try:
      self.driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
      return False
    return True
