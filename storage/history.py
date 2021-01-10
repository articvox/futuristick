import logging
import os
import pickle
from typing import List

HISTORY = os.path.join(os.path.dirname(__file__), 'history.pkl')


def save(content: str) -> None:
    logging.info('Storing content: ' + content)
    history = load_all()
    history.append(content)

    with open(HISTORY, 'wb') as o:
        pickle.dump(history, o, protocol=pickle.HIGHEST_PROTOCOL)
        logging.info('Stored content')


def load_all() -> List[str]:
    try:
        with open(HISTORY, 'rb') as i:
            return pickle.load(i)
    except (FileNotFoundError, EOFError):
        return []
