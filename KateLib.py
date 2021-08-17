from json import load as load_json
from random import randint


class RandomSymbols:
    def __init__(self):
        self.Hearts = ['❤', '🧡', '💛', '💚', '💙', '💜', '🤍']

    def random_heart(self):
        return self.Hearts[randint(0, 6)]


def load_json_file(filename):
    with open(filename, 'r', encoding="utf8") as F:
        return load_json(F)
