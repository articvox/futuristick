from news.article import Article


class ArticleConverter:

    @staticmethod
    def from_soup(soup) -> Article:
        return Article(' '.join(soup.title.string.replace('\n', ' ').split()),
                       soup.description.string.replace('\n', ' '),
                       soup.guid.string,
                       soup.link.string,
                       soup.pubDate.string)
