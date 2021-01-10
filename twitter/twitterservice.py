import logging
from typing import Callable

import tweepy
from tweepy import TweepError


def do_nothing():
    pass


class TwitterService:

    def __init__(self, config: {}):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])

        self.twitterAPI = tweepy.API(auth)

    def post(self, content: str, on_success: Callable) -> None:
        logging.info('Posting tweet: ' + content)

        if len(content) >= 280:
            logging.info('Skipping tweet, content length over 280 characters')
            return

        try:
            self.twitterAPI.update_status(content)
            logging.info('Tweet posted')
            on_success()
        except TweepError as e:
            logging.error('Tweeting failed: ' + e.reason)

    def delete_all(self) -> None:
        for status in tweepy.Cursor(self.twitterAPI.user_timeline).items():
            self.twitterAPI.destroy_status(status.id)
