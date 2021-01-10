class Article:

    def __init__(self, title: str, description: str, guid: str, url: str, published: str):
        self.title = title
        self.description = description
        self.guid = guid
        self.url = url
        self.published = published
        self.keywords = []
