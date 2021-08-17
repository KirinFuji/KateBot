# Written by github.com/KirinFuji

"""
MIT License

Copyright (c) 2021 KirinFuji@users.noreply.github.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from json import load as load_json
from random import randint
from datetime import datetime
from termcolor import colored


class RandomSymbols:
    def __init__(self):
        self.Hearts = ['❤', '🧡', '💛', '💚', '💙', '💜', '🤍']

    def random_heart(self):
        return self.Hearts[randint(0, 6)]


def load_json_file(filename):
    with open(filename, 'r', encoding="utf8") as F:
        return load_json(F)


class Logging:
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.warning = True
        self.error = True
        self.normal = True
        self.enabled = True
        self.milliseconds = False
        self.modules = []

    def timestamp(self):
        if self.milliseconds:
            return datetime.utcnow()
        else:
            return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, module, message, verbose=False, warning=False, debug=False, error=False):
        if self.enabled:
            if self.debug and debug:
                print(colored(f'[{self.timestamp()}][{module}][DEBUG]: {message}', 'blue'))
                return
            elif self.warning and warning:
                print(colored(f'[{self.timestamp()}][{module}][WARN]: {message}', 'yellow'))
                return
            elif self.verbose and verbose:
                print(colored(f'[{self.timestamp()}][{module}]: {message}', 'white'))
                return
            elif self.error and error:
                print(colored(f'[{self.timestamp()}][{module}][ERROR]: {message}', 'red'))
                return
            elif not verbose and not warning and not debug:
                print(f'[{self.timestamp()}][{module}]: {message}')
                return
