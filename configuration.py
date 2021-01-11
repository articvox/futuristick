import json
import logging
import os


class ConfigurationLoader:
    def __init__(self, source: str):
        self.source = source
        self.config = {}
        self.load()

    def load(self) -> None:
        try:
            with open(os.path.join(os.path.dirname(__file__), self.source), 'r') as i:
                self.config = json.load(i)
        except FileNotFoundError:
            logging.error('Configuration file could not be loaded, source missing: ' + self.source)

    def get(self):
        return self.config

    def __str__(self):
        return str(self.config)
