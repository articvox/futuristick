import logging

from configuration import ConfigurationLoader

from counter import Counter
from news.collector import RssItemCollector
from storage.check import Check
from storage.history import save
from twitter.tweet import Tweet
from twitter.twitterservice import TwitterService


def run() -> None:
    logging.info('Checking RSS feeds...')
    counter = Counter()

    for key, rss_config in ConfigurationLoader('config/rss.json').get().items():
        if counter.count >= app_config['max_post_count']:
            break
        logging.info(f'Feed: {key}')

        rss_items = (RssItemCollector(rss_config['url'])
                     .collect()
                     .get_items())

        for rss_item in rss_items:
            if counter.count >= app_config['max_post_count']:
                logging.info(f'Max post count achieved ({counter.count}). Stopping...')
                break

            if not Check.is_posted(rss_item.title):
                hashtags = app_config['constant_tags'] + rss_item.keywords

                if app_config['use_default_tags'] and rss_item['default_tags']:
                    hashtags += rss_item['default_tags']

                tweet = Tweet(
                    rss_item.title,
                    hashtags[0: app_config['max_tags_per_post']]
                )
                tweet = tweet.link(rss_item.url)
                logging.info(f'Tweet candidate: {tweet.descriptor()}')

                twitter.post(
                    tweet.build(),
                    success=lambda: (
                        save(rss_item.title),
                        counter.increment()
                    ),
                    skip=lambda: save(rss_item.title)
                )
            else:
                logging.info(f'Skipping already posted article: {rss_item.title} | guid: {rss_item.guid}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s'
    )

    app_config = ConfigurationLoader('config/properties.json').get()
    twitter = TwitterService(app_config['twitter'])

    run()
