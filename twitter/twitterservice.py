import logging
from typing import Callable

import tweepy
from tweepy import TweepError


class TwitterService:

    def __init__(self, config: {}):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])

        self.twitterAPI = tweepy.API(auth)
        self.max_content_length = config['max_content_length']

    def post(self, content: str, success: Callable, skip: Callable) -> None:
        logging.info('Posting tweet...')

        if len(content) > self.max_content_length:
            logging.info(f'Skipping tweet, content length over {self.max_content_length} characters')
            skip()
            return

        try:
            self.twitterAPI.update_status(content)
            logging.info('Tweet posted successfully')
            success()
        except TweepError as e:
            logging.error('Tweeting failed: ' + e.reason)

    def delete_all(self) -> None:
        for status in tweepy.Cursor(self.twitterAPI.user_timeline).items():
            self.twitterAPI.destroy_status(status.id)
