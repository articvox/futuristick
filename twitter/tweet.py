from __future__ import annotations

from typing import List


class Tweet:

    def __init__(self, content: str, tags: List[str]):
        self.content = content
        self.tags = tags
        self.url = ''
        self.result = f'{self.content} {" ".join(["#" + t for t in self.tags])}'

    def link(self, url: str) -> Tweet:
        self.url = url.strip()
        self.result += f'\n{url}'
        return self

    def build(self) -> str:
        return self.result

    def descriptor(self) -> str:
        return f'\n[Content: {self.content}]' \
               f'\n[Tags: {self.tags}]' \
               f'\n[Link: {self.url}]'
