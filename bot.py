import logging

from config import Config
from news.collector import Collector
from storage.check import Check
from twitter.tweet import Tweet
from twitter.twitterservice import TwitterService

config = Config('properties.json').get()
logging.basicConfig(level=logging.INFO)

ts = TwitterService(config['twitter'])
custom_tags = config['custom_tags']

for feed in config['feeds'].values():
    items = (Collector(feed['rss'])
             .collect()
             .get_items())

    for item in items:
        if not Check.is_posted(item.title):
            keywords = custom_tags + item.keywords
            print(Tweet(item.title, keywords[0: config['max_tag_count']]).link(item.url).build())
            '''
            ts.post(Tweet(item.title, keywords[0: config['max_tag_count']])
                    .link(item.url)
                    .build(),
                    on_success=lambda: save(item.title))'''
        else:
            logging.info('Skipping article title (already posted): ' + item.title)


