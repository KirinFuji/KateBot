# Written by github.com/KirinFuji

#
#     .-.                 .-.
#    (_) )  .'-     /    (_) )-.            /
#       /  /.-. ---/---.-.  / __)  .-._.---/---
#     _/_.'(  |   /  ./.-'_/    `.(   )   /
#  .  /   \ `-'-'/   (__.'/'      )`-'   /
# (_.'     `-'         (_/  `----'

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
from os.path import isfile
from random import randint
from datetime import datetime
from termcolor import colored
from enum import Enum


class RandomSymbols:
    """Library of random Symbols :3"""
    Hearts = ['❤', '🧡', '💛', '💚', '💙', '💜', '🤍']

    @staticmethod
    def random_heart():
        """Why wouldn't you want random hears?"""
        return RandomSymbols.Hearts[randint(0, 6)]


def safe_get(dictionary, *keys):
    """For accessing deeply nested data from dictionaries"""
    for key in keys:
        try:
            dictionary = dictionary[key]
        except KeyError as err:
            print(f"Dictionary KeyError!: {key} : {err}")
            return None
        except AttributeError as err:
            print(f"Nested dictionary encountered non dict-type object @: {key}! : {err}")
            return None
        except TypeError:
            return None
    return dictionary


def load_json_file(filename, logger):
    """Returns a dictionary from json file"""
    exists = isfile(filename)
    if not exists:
        logger.log('KateLib', f"Error Loading Json:\n  -File: {filename}\n  -Valid: {exists}",
                   logger.Type.error)
    else:
        logger.log('KateLib', f"Loading Json:\n  -File: {filename}\n  -Valid: {exists}",
                   logger.Type.debug)
        try:
            with open(filename, 'r', encoding="utf8") as F:
                return load_json(F)
        except UnicodeEncodeError as err:
            logger.log('KateLib', f"Error Loading Json:\n  -{err}", logger.Type.error)


class Log:
    """Custom Logging Class"""

    class Colors(Enum):
        """Enum for logging class colors"""
        grey = 'white',
        blue = 'blue',
        white = None,
        yellow = 'yellow',
        red = 'red'

    class Type(Enum):
        """Enum for logging class type"""
        verbose = 0,
        debug = 1,
        normal = 2,
        warning = 3,
        error = 4,

    def __init__(self):
        # Toggle log types
        self.verbose = False
        self.debug = False
        self.normal = True
        self.warning = True
        self.error = True
        self.enabled = True
        self.milliseconds = False

    def timestamp(self):
        """Create Constant Timestamp"""
        if self.milliseconds:
            return datetime.utcnow()
        else:
            return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, module, message, log_type, tag="", color=None):
        """Log an event to console (To DB in future)
        """
        if log_type is None:
            log_type = self.Type.normal
        if self.enabled:
            if color is not None:
                print(colored(f'[{self.timestamp()}][{module}]{tag}: {message}', color))
            else:
                if self.verbose and log_type == self.Type.verbose:
                    print(colored(f'[{self.timestamp()}][{module}]: {message}', 'white'))
                    return
                elif self.debug and log_type == self.Type.debug:
                    print(colored(f'[{self.timestamp()}][{module}][DEBUG]: {message}', 'blue'))
                    return
                elif self.normal and log_type == self.Type.normal:
                    print(f'[{self.timestamp()}][{module}]: {message}')
                    return
                elif self.warning and log_type == self.Type.warning:
                    print(colored(f'[{self.timestamp()}][{module}][WARN]: {message}', 'yellow'))
                    return
                elif self.error and log_type == self.Type.error:
                    print(colored(f'[{self.timestamp()}][{module}][ERROR]: {message}', 'red'))
                    return
