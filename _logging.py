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
