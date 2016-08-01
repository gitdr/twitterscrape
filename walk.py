from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from create_schema import Base, User, Tweet

import datetime
import os
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pprint

engine = create_engine('sqlite:///tweets.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

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


users = [user.id for user in session.query(User).all()]
tweets_in_db = [tweet.id for tweet in session.query(Tweet).all()]

print users

for folder, subs, files in os.walk("./data"):
  if files:
    f = open(folder + '/' + files[0], 'r')

    html = f.read().decode('utf8')

    f.close()

    parsed_html = BeautifulSoup(html, "lxml")

    lis = parsed_html.find('ol', attrs={'class':'stream-items'}).find_all('li', attrs={'data-item-type':'tweet'})
    
    amt = 0

    for li in lis:
      tweet = parse_tweet_li(li)
      pp.pprint(tweet)
      print "-===========================-"
      amt += 1
      user_id = int(tweet['data-user-id'])
      if not user_id in users:
        # Insert a Person in the person table
        new_user = User(id=tweet['data-user-id'], name=tweet['data-name'], screen_name=tweet['data-screen-name'])
        session.add(new_user)
        users.append(user_id)
        session.commit()
      else:
        user = session.query(User).filter(User.id == user_id).first()
        tweet_id = int(tweet['data-tweet-id'])
        if not tweet_id in tweets_in_db:
          new_tweet = Tweet(id=tweet_id, user=user, tweet_text=tweet['data-tweet-text'], timestamp=datetime.datetime.fromtimestamp(int(tweet['data-time-ms'])/1000))
          session.add(new_tweet)
          tweets_in_db.append(tweet_id)
          session.commit()

       
      # Insert an Address in the address table
      # new_address = Address(post_code='00000', person=new_person)
      # session.add(new_address)
      # session.commit()

    print folder, amt
    

  