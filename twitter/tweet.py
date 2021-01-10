from __future__ import annotations

from typing import List


class Tweet:

    def __init__(self, content: str, tags: List[str]):
        self.content = content
        self.tags = tags
        self.result = f'{self.content} {" ".join(["#" + t for t in self.tags])}'

    def link(self, url: str) -> Tweet:
        self.result += f'\n{url}'
        return self

    def build(self) -> str:
        return self.result
