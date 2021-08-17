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

from datetime import datetime
from termcolor import colored


def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def log(module, message):
    print(colored(f'[{timestamp()}][{module}]: {message}'))


class Logging:
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.warning = True
        self.error = True
        self.normal = True
        self.enabled = True
        self.bot = True
        self.discord = True
        self.reddit = True
        self.music_player = True
        self.modules = []

    def load(self):
        if self.bot:
            self.modules.append('KateBot')
        if self.reddit:
            self.modules.append('Discord')
        if self.reddit:
            self.modules.append('Reddit')
        if self.music_player:
            self.modules.append('MusicBot')

    def log(self, module, message, verbose=False, warning=False, debug=False, error=False, force=False):
        if self.enabled and module in self.modules or force:
            if self.debug and debug:
                print(colored(f'[{timestamp()}][{module}][DEBUG]: {message}', 'blue'))
                return
            elif self.warning and warning:
                print(colored(f'[{timestamp()}][{module}][WARN]: {message}', 'yellow'))
                return
            elif self.verbose and verbose:
                print(colored(f'[{timestamp()}][{module}]: {message}', 'white'))
                return
            elif self.error and error:
                print(colored(f'[{timestamp()}][{module}][ERROR]: {message}', 'red'))
                return
            elif not verbose and not warning and not debug:
                print(f'[{timestamp()}][{module}]: {message}')
                return
