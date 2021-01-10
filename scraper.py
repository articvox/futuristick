import requests
from bs4 import BeautifulSoup

from config import Config
from news.article import Article
from news.articleconverter import ArticleConverter

config = Config('properties.json')

articles = []
feed = BeautifulSoup(requests.get(config.get('rss_feed')).content, 'xml')

for item in feed.find_all('item'):
    articles.append(ArticleConverter.from_soup(item))


