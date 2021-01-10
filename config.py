from __future__ import annotations

import json
import os


class Config:
    def __init__(self, source: str):
        self.source = source
        self.config = {}
        self.load()

    def load(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), self.source), 'r') as i:
            self.config = json.load(i)

    def get(self):
        return self.config

    def __str__(self):
        return str(self.config)
