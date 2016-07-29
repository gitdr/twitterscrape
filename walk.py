import os
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pprint

# rootdir = sys.argv[1]

def merge(dict_a, dict_b):
  z = dict_a.copy()
  z.update(dict_b)
  return z

pp = pprint.PrettyPrinter(indent=4)


def parse_tweet_li(li):
  if isinstance(li, NavigableString):
    if not li.string.isspace():
      print li.string
  else:
    data = merge(li.attrs, li.find('div').attrs)
    timestamp_el = li.find('div').find('span', attrs={'class':'_timestamp'})
    data = merge(data, timestamp_el.attrs)

    unwanted = set(data) - set(['data-tweet-id','data-name','data-screen-name','data-time-ms','data-user-id','data-permalink-path'])
    for unwanted_key in unwanted: del data[unwanted_key]

    list = [];

    for el in li.find('p', attrs={'class':'js-tweet-text'}).descendants:
      if isinstance(el, NavigableString):
        list.append(el.string.rstrip())

    data['data-tweet-text'] = ' '.join(list)

    img_div = li.find('div', attrs={'class':'js-adaptive-photo'})

    if img_div:
      data['picture'] = (img_div.attrs)['data-image-url']

    return data 

for folder, subs, files in os.walk("./data"):
  if files:
    f = open(folder + '/' + files[0], 'r')

    html = f.read().decode('utf8')

    f.close()

    parsed_html = BeautifulSoup(html, "lxml")

    lis = parsed_html.find('ol', attrs={'class':'stream-items'}).find_all('li', attrs={'data-item-type':'tweet'})
    
    amt = 0

    for li in lis:
      pp.pprint(parse_tweet_li(li))
      print "-===========================-"
      amt += 1

    print folder, amt
    

  