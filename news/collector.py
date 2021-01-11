from __future__ import annotations

import logging
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from news.article import Article
from news.articleconverter import ArticleConverter


class KeywordCollector:
    __ATTRS = {
        'name': ['keywords', 'news_keywords']
    }

    @staticmethod
    def to_list(keywords: str) -> List[str]:
        return re.split('[;,]', keywords) if keywords else []

    @staticmethod
    def normalize(value: str) -> str:
        return (value
                .replace(' ', '')
                .replace('-', '')) if value else value

    @staticmethod
    def is_valid(keyword: str) -> bool:
        return all(x not in keyword for x in ["'", ".", ","]) and len(keyword) < 20

    @staticmethod
    def from_article(url: str) -> List[str]:
        keywords = ''
        try:
            source = BeautifulSoup(requests.get(url).content, 'html.parser')
            meta_keywords = source.find(attrs=KeywordCollector.__ATTRS)

            keywords = meta_keywords['content'] if meta_keywords else keywords
        except requests.RequestException as e:
            logging.error(f'Could not retrieve the news article for keyword scraping: {url} {e}')

        return [KeywordCollector.normalize(key) for key in KeywordCollector.to_list(keywords) if
                KeywordCollector.is_valid(key)]


class RssItemCollector:
    __RSS_ITEM = 'item'

    def __init__(self, source: str):
        self.source = source
        self.rss_items = []

    def collect(self) -> RssItemCollector:
        try:
            feed = BeautifulSoup(requests.get(self.source).content, 'xml')

            for item in feed.find_all(self.__RSS_ITEM):
                article = ArticleConverter.from_soup(item)
                article.keywords = KeywordCollector.from_article(article.url)

                self.rss_items.append(article)
        except requests.RequestException as e:
            logging.error(f'Could not retrieve the RSS feed for: {self.source} {e}')

        return self

    def get_items(self) -> List[Article]:
        return self.rss_items
