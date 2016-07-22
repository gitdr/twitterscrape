from bs4 import BeautifulSoup
import logging

class Parser:

  def __init__(self):
    self.log = logging.getLogger('twitterscrape.parser')

  def test_log(self, str):
    self.log.info(str)

  def parse(self, html):
    parsed_html = BeautifulSoup(html, "lxml")

    f = open('twitterpage.html', 'w')

    f.write(html.encode('utf8'))

    f.close()

    for el in parsed_html.body.find_all('strong', attrs={'class':'fullname'}):
      print el.text

    # print parsed_html.body.find_all('strong', attrs={'class':'fullname'}).text
    # print parsed_html.body.find_all('span', attrs={'class':'_timestamp'}).attrs['data-time']
    # print parsed_html.body.find_all('div', attrs={'class':'js-tweet-text-container'}).text
