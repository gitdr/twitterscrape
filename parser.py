import logging

class Parser:

  def __init__(self):
    self.log = logging.getLogger('twitterscrape.parser')

  def test_log(self, str):
    self.log.info(str)