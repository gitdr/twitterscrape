from bs4 import BeautifulSoup

f = open('twitterpage.html', 'r')

html = f.read().decode('utf8')

f.close()

parsed_html = BeautifulSoup(html, "lxml")

for el in parsed_html.body.find_all('strong', attrs={'class':'fullname'}):
  print el.text

for el in parsed_html.body.find_all('span', attrs={'class':'_timestamp'}):
  print el.attrs['data-time']

for el in parsed_html.body.find_all('div', attrs={'class':'js-tweet-text-container'}):
  print el.text

# print parsed_html.body.find('strong', attrs={'class':'fullname'}).text
# print parsed_html.body.find('span', attrs={'class':'_timestamp'}).attrs['data-time']
# print parsed_html.body.find('div', attrs={'class':'js-tweet-text-container'}).text