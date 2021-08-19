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


# Static Class example
class RandomSymbols:
    """Library of random Symbols :3"""
    Hearts = ['❤', '🧡', '💛', '💚', '💙', '💜', '🤍']

    @staticmethod
    def random_heart():
        """Why wouldn't you want random hears?"""
        return RandomSymbols.Hearts[randint(0, len(RandomSymbols.Hearts))]


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


def load_json_file(filename):
    """Returns a dictionary from json file"""
    exists = isfile(filename)
    if not exists:
        Log.log('KateLib', f"Error Loading Json:\n  -File: {filename}\n  -Valid: {exists}",
                Log.Type.error)
    else:
        Log.log('KateLib', f"Loading Json:\n  -File: {filename}\n  -Valid: {exists}",
                Log.Type.debug)
        try:
            with open(filename, 'r', encoding="utf8") as F:
                return load_json(F)
        except UnicodeEncodeError as err:
            Log.log('KateLib', f"Error Loading Json:\n  -{err}", Log.Type.error)


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

    # Toggle log types
    verbose = False
    debug = False
    normal = True
    warning = True
    error = True
    enabled = True
    milliseconds = False

    @staticmethod
    def timestamp():
        """Create Consistent Timestamp"""
        if Log.milliseconds:
            return datetime.utcnow()
        else:
            return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def log(cls, module, message, log_type, tag="", color=None):
        """Log an event to console (To DB in future)
        """
        if log_type is None:
            log_type = cls.Type.normal
        if cls.enabled:
            if color is not None:
                print(colored(f'[{cls.timestamp()}][{module}]{tag}: {message}', color))
            else:
                if cls.verbose and log_type == cls.Type.verbose:
                    print(colored(f'[{cls.timestamp()}][{module}]: {message}', 'white'))
                    return
                elif cls.debug and log_type == cls.Type.debug:
                    print(colored(f'[{cls.timestamp()}][{module}][DEBUG]: {message}', 'blue'))
                    return
                elif cls.normal and log_type == cls.Type.normal:
                    print(f'[{cls.timestamp()}][{module}]: {message}')
                    return
                elif cls.warning and log_type == cls.Type.warning:
                    print(colored(f'[{cls.timestamp()}][{module}][WARN]: {message}', 'yellow'))
                    return
                elif cls.error and log_type == cls.Type.error:
                    print(colored(f'[{cls.timestamp()}][{module}][ERROR]: {message}', 'red'))
                    return
