from __future__ import annotations

import re
from typing import List

import requests
from bs4 import BeautifulSoup

from news.article import Article
from news.articleconverter import ArticleConverter


def normalize(value: str) -> str:
    return (value
            .replace(' ', '')
            .replace('-', ''))


def as_list(keywords: str) -> List[str]:
    return re.split(';|,', keywords)


def find_keywords(url) -> List[str]:
    source = BeautifulSoup(requests.get(url).content, 'html.parser')
    keywords = source.find(attrs={'name': ['keywords', 'news_keywords']})['content']

    if not keywords:
        return []

    return [normalize(keyword) for keyword in as_list(keywords) if "'" not in keyword and len(keyword) < 20]


class Collector:
    RSS_ITEM = 'item'

    def __init__(self, source: str):
        self.source = source
        self.items = []

    def collect(self) -> Collector:
        feed = BeautifulSoup(requests.get(self.source).content, 'xml')

        for item in feed.find_all(self.RSS_ITEM):
            article = ArticleConverter.from_soup(item)
            article.keywords = find_keywords(article.url)

            self.items.append(article)

        return self

    def get_items(self) -> List[Article]:
        return self.items
