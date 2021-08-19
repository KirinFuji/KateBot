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

# NOTICE #
# PyNaCl library needed in order to use MusicPlayer
from os.path import isdir
import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from KateLib import load_json_file, RandomSymbols, Log
from functools import wraps
from shutil import copytree

# Windows Development Fix
# Big thanks to https://github.com/paaksing for this snippet!
# https://github.com/aio-libs/aiohttp/issues/4324
# http://www.apache.org/licenses/LICENSE-2.0
import platform
# Protected member is being patched as a bug fix.
# noinspection PyProtectedMember
from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    """ This code serves to fix a crash that specifically happens on windows due to the aiohttp
    library using a different underlying mechanism on windows. See issue 4324 for more information."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wraps the incoming function with an exception handler"""

        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


if platform.system() == 'Windows':
    # Silence the exception here.
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
# End Windows Development Fix


class KateBot(commands.Bot):
    """Discord.py Bot Extension"""

    def __init__(self):
        # Create Dictionary from discord.json
        config = load_json_file('config/discord.json')
        self.token = config['token']
        if self.token == "<token>":
            raise ValueError("You must fill out discord.json!!")
        # Setup Gateway Intents
        intent = discord.Intents.default()
        intent.members = config['members_intent']
        intent.typing = config['typing_intent']
        intent.presences = config['presences_intent']
        # Initialize inherited Bot class
        commands.Bot.__init__(self,
                              owner_ids=config['owner_ids'],
                              command_prefix=config['prefix'],
                              case_insensitive=config['case_insensitive'],
                              intents=intent)
        # Initialize additional objects
        self.tasks = []
        Log.log("KateBot", "Initialized", Log.Type.debug)

    async def on_ready(self):
        """Runs when successfully connected to Discord API"""
        Log.log('Discord', f'Logged in as {self.user}! {RandomSymbols.random_heart()}', None)

    @staticmethod
    async def on_disconnect():
        """For seeing if any issues arise by timestamping the disconnects"""
        Log.log('Discord', 'Disconnected', Log.Type.warning)

    async def on_command_error(self, ctx, error):
        """Create Exception Handler for command errors"""
        Log.log("Discord", f"{error}\n"
                            f" Author: [{ctx.author}]\n"
                            f" Channel: [{ctx.channel}]",
                            Log.Type.error)

    async def set_listening(self, text):
        """Changes discord presence to listening to <song>"""
        da = discord.ActivityType
        await self.change_presence(activity=discord.Activity(type=da.listening, name=text.replace('.mp3', '')))

    async def set_idle(self):
        """Removes discord presence"""
        da = discord.ActivityType
        await self.change_presence(activity=discord.Activity(type=da.listening, name=''))


if __name__ == '__main__':
    if not isdir('config/'):
        try:
            copytree('config-samples', 'config')
        except FileExistsError:
            pass
        except OSError as err:
            print(f"Error Creating Config Directory: {err}")
        print("Config Files Generated @ config/ please fill them out!")
        exit(1)

    RandomSymbols.Hearts.append('Test')
    RandomSymbols.Hearts.append('Test1')
    RandomSymbols.Hearts.append('Test2')
    RandomSymbols.Hearts.append('Test3')
    RandomSymbols.Hearts.append('Test4')
    RandomSymbols.Hearts.append('Test5')

    # SQL Alchemy Setup
    engine = create_engine(f"sqlite:///database.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Logging Setup

    Log.debug = False
    Log.verbose = False
    Log.milliseconds = True

    # KateBot Setup
    KBot = KateBot()
    KBot.load_extension("cogs.administrative")
    KBot.load_extension("cogs.music_player")
    KBot.load_extension("cogs.reddit")
    KBot.load_extension("cogs.reaction_roles")
    KBot.load_extension('cogs.crypto_coins')

    # KBot.get_cog('reddit')

    # Entry Point
    KBot.run(KBot.token)
